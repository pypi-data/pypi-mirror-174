from buildpack import Buildpack
bp = Buildpack(f"myapp")
if __name__ == "__main__":
    print(bp.dockerfiles(language="python", port=8000, entrypoint="app"))