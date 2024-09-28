from fasthtml import common as fh

app = fh.FastHTML()


@app.get("/")
def home():
    return (
        fh.Title("Basic site"),
        fh.Main(fh.H1("Title", style="font-size:20px;  color:red;")),
    )


fh.serve()
