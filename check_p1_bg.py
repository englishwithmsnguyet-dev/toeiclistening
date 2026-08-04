import pptx
prs = pptx.Presentation('../TOEIC LISTENING - PART 01.pptx')
slide = prs.slides[206]
print("Background fill type:", slide.background.fill.type)
