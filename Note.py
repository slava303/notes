class Note:
    def __init__(self, id, dtime, header, txt):
        self.id = id
        self.dtime = dtime
        self.header = header
        self.txt = txt

    def header_preview(self, length):
        return self.header[:length] + '...' if len(self.header) > length else self.header.ljust(length + 3)

    def txt_preview(self, length):
        preview = self.txt[:length] + '...' if len(self.txt) > length else self.txt.ljust(length + 3)
        return preview.replace("\n", " ").replace("\r", "").replace("\t", " ")