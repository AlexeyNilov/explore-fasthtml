from fasthtml import common as fh


flex_grid = fh.Link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
)
htmx_ws = fh.Script(src="https://unpkg.com/htmx-ext-ws@2.0.0/ws.js")
style = "{ border: 1px solid black; border-radius: 5px; margin: 2px; padding: 2px; }"
css = fh.Style(
    f"""
    .row {style}
    .box {style}
    .col-xs-3 {style}
    .col-xs-4 {style}
    .col-xs {style}
    #event-list p {{ margin: 1px; padding: 1px;}}
    progress::-webkit-progress-value {{ background-color: red !important; }}
"""
)
headers = (fh.picolink, flex_grid, htmx_ws, css)
