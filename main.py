import os
from glob import glob
from srt import parse
from tempfile import NamedTemporaryFile


class TmpFile:
    mode = dict(mode='rt', encoding='utf-8')

    def __init__(self):
        pass

    def __exit__(self, type, value, tb):
        self.f.close()
        os.remove(self.f.name)

    def __enter__(self):
        self.f = NamedTemporaryFile(delete=False, **TmpFile.mode)
        return self

    def borrow_name(self, proc):
        self.f.close()
        proc(self.f.name)
        self.f = open(self.f.name, **TmpFile.mode)
        return self

    def readlines(self):
        return self.f.readlines()


def proceed(file_name, index_pair=(3, 4)):
    with TmpFile() as tmp_file,\
        open(os.path.join(file_name[:-3]+"srt"),
             mode="w", encoding="utf-8", newline="\r\n") as out_file:
        (donor, recipient) = [parse(
            tmp_file.borrow_name(
                lambda name:os.system(
                    "mkvextract tracks {} {}:{}".format(file_name, track_index, name))
            ).readlines()
        ) for track_index in index_pair]

        augs = []
        for rcpnt in recipient:
            augs = [a for a in augs if a.end > rcpnt.beg]
            while len(donor) > 0 and donor[0].beg < rcpnt.end:
                augs.append(donor.pop(0))
            if len(augs) > 0:
                rcpnt.text += "\n \n" + '\n'.join(a.text for a in augs)
            out_file.write(str(rcpnt))


if __name__ == '__main__':
    path = '.'
    for file_name in glob(os.path.join(path, "*.mkv")):
        proceed(file_name)
