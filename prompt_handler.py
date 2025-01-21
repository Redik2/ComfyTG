def txt2prompt(text: str):
    prompt = {}
    text = text.replace("/txt2img ", "")
    raw_tags = text.split("--")
    
    prompt["model"] = raw_tags[0][:-1]

    parameters = {}
    for tag in raw_tags[1:]:
        name = tag.split()[0]
        value = " ".join(tag.split()[1:])

        parameters[name] = value
    
    prompt["parameters"] = parameters

    return prompt


if __name__ == "__main__":
    print(txt2prompt("/txt2img test model idk --positive 1girl, casual clothing --negative worst quality, low quality"))