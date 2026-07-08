{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, flake-utils, nixpkgs, ... }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs { inherit system; };
        nc-py-api = pkgs.python3Packages.buildPythonPackage rec {
          pname = "nc_py_api";
          version = "0.30.2";
          pyproject = true;

          src = pkgs.python3Packages.fetchPypi {
            inherit pname version;
            hash = "sha256-jk9QThogBHXcIm2xuC0OGIgP2K59NK08QTPmYCFgafI=";
          };

          nativeBuildInputs = with pkgs.python3Packages; [
            hatch-build-scripts
          ];

          propagatedBuildInputs = with pkgs.python3Packages; [
            caldav
            fastapi
            filelock
            niquests
            pydantic
            python-dotenv
            starlette
            xmltodict
          ];

          doCheck = false;
        };
        python3 = pkgs.python3.withPackages (pypkgs: with pypkgs; [
          nc-py-api
        ]);
      in {
        devShell = pkgs.mkShell {
          name = "academy_dev_devenv";
          packages = (with pkgs; [
            basedpyright
            python3
            ruff
          ]);
        };
      }
    );
}
