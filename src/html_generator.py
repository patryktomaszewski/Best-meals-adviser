from jinja2 import Environment, FileSystemLoader


def get_html_title(data):
    path = ''
    for meal in data:
        for used in data[meal]['usedIngredients']:
            used = used.replace(' ', '')
            eng = used.split("/", 1)
            path = path + str.lower(eng[0]) + '_'
        for used in data[meal]['missedIngredients']:
            missed = used.replace(' ', '')
            eng = missed.split("/", 1)
            path = path + str.lower(eng[0]) + '_'

    final_path = path[:-1]
    return '../recipes/' + final_path + '.html'


def get_html(data):

    best_meal = data.pop('Best Meal Option')
    env = Environment(loader=FileSystemLoader('html_templates'))
    template = env.get_template('recipes_template.html')
    output_from_parsed_template = template.render(data=data, best_meal=best_meal)

    path = get_html_title(data)

    with open(path, "w") as fh:
        fh.write(output_from_parsed_template)
    fh.close()