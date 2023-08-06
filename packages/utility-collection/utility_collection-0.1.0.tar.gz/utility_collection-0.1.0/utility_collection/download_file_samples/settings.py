BASE_URL: str = "https://filesamples.com/samples/"

SAMPLES: dict[str, dict[str, list[str]]] = {
    "document": {
        "doc": ["sample1.doc"],
        "docx": ["sample1.docx"],
        "pdf": ["sample1.pdf"],
        "ppt": ["sample1.ppt"],
        "txt": ["sample1.txt"],
        "xls": ["sample1.xls"],
        "xlsx": ["sample1.xlsx"],
    },
    "video": {
        "mp4": [
            "sample_1280x720_surfing_with_audio.mp4",
            "sample_1280x720.mp4",
            "sample_1920x1080.mp4",
            "sample_2560x1440.mp4",
            "sample_3840x2160.mp4",
            "sample_640x360.mp4",
            "sample_960x400_ocean_with_audio.mp4",
            "sample_960x540.mp4",
        ]
    },
}
