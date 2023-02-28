from pyproject_template.pyproject_template import main


def test_main(capsys):
    main()
    captured = capsys.readouterr()

    assert captured.out == "Hello world!\n"
