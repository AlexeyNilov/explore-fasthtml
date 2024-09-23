from fasthtml.common import FastHTMLWithLiveReload, serve, Html, Head, Title, Body, Div, A, Img

app = FastHTMLWithLiveReload()


@app.get("/")
def home():
    page = Html(
        Head(Title('Main app')),
        Body(Div('Some text, ', A('A link', href='https://example.com'), Img(src="https://placehold.co/200"), cls='myclass')))
    return page


serve()
