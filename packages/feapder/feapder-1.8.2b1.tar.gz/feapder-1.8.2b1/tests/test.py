import feapder

html = "<a href='/666'>hello word</a>"
response = feapder.Response.from_text(text=html)
print(response.xpath("//a/@href").extract_first())
