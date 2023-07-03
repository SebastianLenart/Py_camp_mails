import click # cos ala args

def is_adult(ctx, param, value):
    if value is None:
        return value
    if value < 18:
        raise click.BadParameter("it should be >= 18")
    return value


@click.command()
@click.option('--age', type=click.INT, callback=is_adult)
@click.option('--ask-for-name', is_flag=True)
@click.option('--save-dir', type=click.Path(exists=True))
@click.option('--language', type=click.Choice(['php', 'python'], case_sensitive=False))
def main(age, ask_for_name, save_dir, language):
    print(age)
    click.echo(age)
    click.echo(ask_for_name)
    click.echo(save_dir)
    click.echo(language)

if __name__ == "__main__":
    main()


# python click_.py --age 19
# python click_.py --age 19 --ask-for-name True
# python click_.py --age 19 False
# python click_.py --save-dir abc
# python click_.py --language pascal # error
# python click_.py --language php
