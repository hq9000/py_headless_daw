from py_headless_daw.project.project import Project
from pathlib import Path


class RidingOnBugs:
    def render(self, output_file: str):
        logging.info('starter rendering RidingOnBugs demo')
        pass


if __name__ == '__main__':
    demo = RidingOnBugs()
    out_file = str(Path(__file__).parent.absolute()) + "/output/out.wav"
    demo.render(out_file)
