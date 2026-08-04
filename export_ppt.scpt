tell application "Microsoft PowerPoint"
    activate
    open POSIX file "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/TOEIC LISTENING - PART 01.pptx"
    set thePres to active presentation
    save thePres in POSIX file "/Users/nguyetpham/Desktop/TEACHING/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/graphics/slides" as save as JPG
    -- Wait a bit for it to finish
    delay 5
    close thePres
end tell
