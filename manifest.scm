(use-modules (guix inferior)
             (guix channels))

(define channels
  (list
    (channel
      (name 'guix)
      (url "https://codeberg.org/guix/guix.git")
      (branch "master")
      (commit
        "0689ad6dd09ca212f5b62efcbe6ac2921cf2b03a")
      (introduction
        (make-channel-introduction
          "9edb3f66fd807b096b48283debdcddccfea34bad"
          (openpgp-fingerprint
            "BBB0 2DDF 2CEA F6A8 0D1D  E643 A2A0 6DF2 A33A 54FA"))))))

(define inferior (inferior-for-channels channels))

(packages->manifest
  (map (lambda (pkg-name)
         (car (lookup-inferior-packages inferior pkg-name)))
    (list
      "python"
      "python-hy"
      "python-grpcio"
      "python-grpcio-tools"
      "python-matplotlib")))
