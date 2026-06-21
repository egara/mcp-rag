{
  description = "mcp-rag — MCP for searching in a RAG created by PostgreSQL and pgvector";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }:
  let
    system = "x86_64-linux";
  in
  {
    devShells."${system}".default =
    let
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
    in
    pkgs.mkShell {
      packages = with pkgs; [
        python313
        python313Packages.pip
        python313Packages.setuptools
        python313Packages.virtualenv
        python313Packages.psycopg2
      ];

      shellHook = ''
        echo "Entering mcp-rag development environment"

        VENV=venv
        if test ! -d $VENV; then
          python -m venv $VENV
        fi
        source ./$VENV/bin/activate

        echo "Installing dependencies from requirements.txt and package..."
        pip install -r requirements.txt
        pip install -e .

        export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
          pkgs.stdenv.cc.cc.lib
          pkgs.zlib
          pkgs.glib
        ]}:$LD_LIBRARY_PATH

      '';
    };
  };
}
