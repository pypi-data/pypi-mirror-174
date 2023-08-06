from requests import get
from bs4 import BeautifulSoup
from reportlab.platypus import Paragraph, SimpleDocTemplate

class Wikipedia2PDF:
    def __init__(self, url: str, filename: str = None) -> None:
        self.url: str = url
        self.filename = filename
        self._converter()

    def extract_article(self, headers: dict = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}):
        res: dict = dict(title = "", description = "")

        page_source: str = get(self.url, headers=headers).text

        parser = BeautifulSoup(page_source, "html.parser")

        res["title"] = parser.find("span", attrs={"class" : "mw-page-title-main"}).text

        ptags: list = parser.findAll("p", attrs={"class" : None, "id" : None})

        for ptag in ptags:
            if len(ptag.text) < 20:
                continue
            res["description"] += ptag.text

        return res

    def _converter(self):
        data: dict = self.extract_article()

        content: str = f"<font size=\"16\"><strong>{data['title']}</strong><br></br><br></br></font><font size=\"14\">{data['description']}</font>" 

        if self.filename and self.filename[-4:] == ".pdf":
            pass
        else:
            self.filename = f"{data['title']}.pdf"

        SimpleDocTemplate(self.filename).build([Paragraph(content)])