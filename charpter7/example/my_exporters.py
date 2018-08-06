from scrapy.exporters import BaseItemExporter
import xlwt


class ExcelItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file
        self.wbook = xlwt.Workbook()
        self.wsheet = self.wbook.add_sheet('scrapy')
        self.row = 0

    def finish_exporting(self):
        self.wbook.save(self.file)

    def export_item(self, item):
        fields = self._get_serialized_fields(item)
        for col, v in enumerate(x for _, x in fields):
            self.wsheet.write(self.row, col, v)
        self.row += 1