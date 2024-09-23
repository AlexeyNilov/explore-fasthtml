from fasthtml.common import (
    FastHTMLWithLiveReload,
    serve,
    Html,
    Head,
    Title,
    Body,
    Div,
    A,
    Img,
    H1,
    Meta,
)

app = FastHTMLWithLiveReload()


@app.get("/")
def home():
    page = Html(
        Head(Title("Main app"), Meta(http_equiv="refresh", content="5")),
        H1("Header"),
        Body(
            Div(
                "Some text, ",
                A("A link", href="https://example.com"),
                Img(src="https://placehold.co/200"),
                cls="myclass",
            )
        ),
    )
    return page


serve()
