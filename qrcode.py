import zxing

reader = zxing.BarCodeReader()
barcode = reader.decode("test.png")
print(barcode.parsed)
