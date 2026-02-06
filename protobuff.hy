;; https://grpc.io/docs/languages/python/quickstart/

(eval-and-compile
  (import subprocess)
  (import pathlib)
  (import functools)

  (defn generate-python [path]
    (let [p (pathlib.Path path)]
      (subprocess.run
        ["python3" "-m" "grpc_tools.protoc"
         (+ "-I" (str p.parent)) "--python_out=." "--pyi_out=." "--grpc_python_out=."
         path])))

  (defn generate-proto [path content]
    (with [f (open path "w")]
      (.write f content)))

  (defn replace-proto-name-sequence [bound-name actual-name sequence]
     (map (fn [f] (replace-proto-name bound-name actual-name f)) sequence))

  (defn replace-proto-name [bound-name actual-name form]
    (cond
      (and (isinstance form hy.models.Expression)
           (= '. (get form 0))
           (= bound-name (get form 1)))
      `(. ~actual-name ~@(cut form 2 (len form)))

      (isinstance form hy.models.Expression)
      `(~@(replace-proto-name-sequence bound-name actual-name form))

      (isinstance form hy.models.List)
      `[~@(replace-proto-name-sequence bound-name actual-name form)]

      ;; TODO: There are more cases, but this is just an example.
      True form))

  (defn add-proto-prefix-sequence [message-set prefix sequence]
     (map (fn [f] (add-proto-prefix message-set prefix f)) sequence))

  (defn add-proto-prefix [message-set prefix form]
    (cond
      (in form message-set)
      `(. ~prefix ~form)

      (isinstance form hy.models.Expression)
      `(~@(add-proto-prefix-sequence message-set prefix form))

      (isinstance form hy.models.List)
      `[~@(add-proto-prefix-sequence message-set prefix form)]

      ;; TODO: There are more cases, but this is just an example.
      True form))

  (defn proto-path->name [class-name path]
    (let [basename (hy.I.pathlib.Path path)]
      [(hy.models.Symbol (+ basename.stem "_pb2"))
       `(. ~(hy.models.Symbol (+ basename.stem "_pb2_grpc"))
           ~(hy.models.Symbol (+ (str class-name) "Servicer")))]))

  (defn defmessage? [form]
    (and (isinstance form hy.models.Expression)
         (= 'defmessage (get form 0))))

  (defn collect-messages [body]
    [(lfor form body
           :if (defmessage? form)
        form)
     (lfor form body
           :if (not (defmessage? form))
        form)])

  (defn message-names [messages]
    (let [acc #{}]
      (functools.reduce
        (fn [acc message]
          (let [name (get message 1)]
            (if (in name acc)
              (raise (ValueError (+ "Duplicate message definition: " name)))
              (do (.add acc name)
                acc))))
        messages
        acc)
      acc))

  (defn class-template [name superclass body]
    `(defclass ~name [~superclass] ~@body))

  (defn proto-message-attribute [attribute]
    (let [[attr-name definition] attribute]
      (if (isinstance definition hy.models.List)
        (do
          (when (!= 2 (len definition))
            (raise (ValueError "When attribute value is a list, it must have exactly the type and the default value.")))
          (let [[attr-type default-value] definition]
            (+ "    " (str attr-type) " " (str attr-name) " = " (str (hy.eval default-value)) ";\n")))
        (+ "    " (str definition) " " (str attr-name) ";\n"))))

  (defn proto-message [_ name body]
    (+ "message " (str name) " {\n"
      (functools.reduce (fn [acc attribute] (+ acc (proto-message-attribute attribute)))
                        (.items body)
                        "")
      "}\n\n"))

  (defn proto-rpc [_defn header args #* _body]
    ;; TODO: better error-checking
    (let [[_ann0 name return-type] header
          [_self request _other] args
          [_ann1 _arg-name request-type] request]
      (+ "    rpc " (str name) " (" (str request-type) ") returns ("
         (str return-type) ") {}\n" )))

  (defn proto-template [name package-name messages rpcs]
    ;; TODO: check that all RPCs are defn forms
    (+ "syntax = \"proto3\";\n"
       f"package {package-name};\n\n"
       (functools.reduce (fn [acc m] (+ acc (proto-message #* m)))
                         messages
                         "")
       "service " (str name) " {\n"
       (functools.reduce (fn [acc rpc] (+ acc (proto-rpc #* rpc)))
                         rpcs
                         "")
       "}\n")))

(defmacro defproto [class-name proto-path #* body]
  (let [[messages body*] (collect-messages body)]
    (when (not (isinstance proto-path hy.models.List))
      (raise (SyntaxError "Proto file binding must be a list.")))
    (when (!= 2 (len proto-path))
      (raise (SyntaxError "Proto file binding must have two elements.")))
    (when (not (isinstance (get proto-path 1) str))
      (raise (SyntaxError "Right-hand side of proto file binding must be a string.")))
    (cond
      (isinstance (get proto-path 0) hy.models.Symbol)
      (do
        (when messages
          (raise (SyntaxError "Cannot define messages when using an external proto.")))
        (when (not (.exists (hy.I.pathlib.Path (get proto-path 1))))
          (raise (ValueError "Proto file does not exist.")))
        (let [[binding path] proto-path
              [inner-name superclass] (proto-path->name class-name path)
              class-form (replace-proto-name binding inner-name
                           (class-template class-name superclass body*))
              python-gen-result (generate-python path)] ;; Runs during macro expansion
          (when (!= 0 python-gen-result.returncode)
            (raise (Exception "Could not generate Python files.")))
          `(do
             (import ~inner-name)
             (import ~(get superclass 1))
             ~class-form)))

      (= (get proto-path 0) :generate)
      (let [[_generate path] proto-path
            [inner-name superclass] (proto-path->name class-name path)
            message-set (message-names messages)
            class-form (add-proto-prefix message-set inner-name
                           (class-template class-name superclass body*))
            basename (hy.I.pathlib.Path path)
            _ (generate-proto path
                (proto-template class-name basename.stem
                  messages
                  body*))
            python-gen-result (generate-python path)]
        (when (!= 0 python-gen-result.returncode)
          (raise (Exception "Could not generate Python files.")))
        `(do
           (import ~inner-name)
           (import ~(get superclass 1))
           ~class-form))

      True
      (raise (SyntaxError "Left-hand side of proto file binding must be a symbol or :generate.")))))

(defproto Dismisser [:generate "./goodbyeworld.proto"]
  (defmessage GoodbyeRequest {name [string 1]})
  (defmessage GoodbyeReply {message [string 1]})
  (defn #^ GoodbyeReply SayGoodbye [self, #^ GoodbyeRequest request _context]
    (GoodbyeReply :message f"Goodbye, {request.name}!")))

(defproto Greeter [MyProto "../protos/helloworld.proto"]
  (defn #^ MyProto.HelloReply SayHello [self #^ MyProto.HelloRequest request _context]
    (MyProto.HelloReply :message f"Hello, {request.name}!")))
