def txt2parameters(text: str):
    parameters = {}
    text = text.replace("/config ", "")
    raw_tags = text.split("--")
    
    parameters["model"] = raw_tags[0][:-1]

    for tag in raw_tags[1:]:
        name = tag.split()[0]
        value = " ".join(tag.split()[1:])

        parameters[name] = value

    return parameters


if __name__ == "__main__":
    print(txt2prompt("/txt2img test model idk --positive 1girl, casual clothing --negative worst quality, low quality"))