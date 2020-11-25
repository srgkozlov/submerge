from dataclasses import dataclass
import os


@dataclass
class Record:
    num: str
    beg: str
    end: str
    text: str

    def __str__(self):
        return "\n".join( [self.num , self.beg + r' --> ' + self.end, self.text, "\n"])


def parse(lines):
    p = []

    def num(line):
        if not line:
            return None
        else:
            p.append(Record(line,'','',''))
            return stamp

    def stamp(line):
        p[-1].beg = line[:12]
        p[-1].end = line[-12:]
        return text

    def text(line):
        if not line:
            return num
        p[-1].text += "\n"+line if (p[-1].text) else line
        return text

    do = num
    for line in lines:
        r = do(line.strip())
        if r:
            do = r
        else:
            break
    return p
