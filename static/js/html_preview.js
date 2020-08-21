let converter = new showdown.Converter();

function convert_markdown_to_html(markdown_markup) {
    return converter.makeHtml(markdown_markup);
}

function html_preview(markdown_field, html_preview_field) {
    markdown_field.addEventListener("keydown", function () {
        html_preview_field.innerHTML = convert_markdown_to_html(markdown_field.value);
    });
}
