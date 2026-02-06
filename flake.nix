{
  description = "Simple flake for dealing with Python 3";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/master";

  outputs =
    { self, nixpkgs, flake-utils }:

    flake-utils.lib.eachDefaultSystem
      (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python313;
      in
      {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = [ pkgs.bashInteractive ];
          buildInputs = with pythonPackages; [
            python
            pythonPackages.matplotlib
            pythonPackages.numpy
          ];
        };
      });
}
