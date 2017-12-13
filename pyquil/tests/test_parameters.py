from math import pi

from pyquil.parameters import Parameter, sin, _contained_parameters, format_parameter


def test_format_parameter():
    test_cases = [
        (1, '1'),
        (1.0, '1.0'),

        (1j, 'i'),
        (0 + 1j, 'i'),
        (-1j, '-i'),
    ]

    for test_case in test_cases:
        assert format_parameter(test_case[0]) == test_case[1]


# https://github.com/rigetticomputing/pyquil/issues/184
def test_pretty_print_pi():
    test_cases = [
        (0., '0'),
        (pi, 'pi'),
        (-pi, '-pi'),
        (2 * pi / 3., '2*pi/3'),
        (pi / 9, '0.3490658503988659'),
        (pi / 8, 'pi/8'),
        (-90 * pi / 2, '-45*pi'),
    ]

    for test_case in test_cases:
        assert format_parameter(test_case[0]) == test_case[1]


def test_expression_to_string():
    x = Parameter('x')
    assert str(x) == '%x'

    y = Parameter('y')
    assert str(y) == '%y'

    assert str(x + y) == '%x+%y'
    assert str(3 * x + y) == '3*%x+%y'
    assert str(3 * (x + y)) == '3*(%x+%y)'

    assert str(x + y + 2) == '%x+%y+2'
    assert str(x - y - 2) == '%x-%y-2'
    assert str(x - (y - 2)) == '%x-(%y-2)'

    assert str((x + y) - 2) == '%x+%y-2'
    assert str(x + (y - 2)) == '%x+%y-2'

    assert str(x ** y ** 2) == '%x^%y^2'
    assert str(x ** (y ** 2)) == '%x^%y^2'
    assert str((x ** y) ** 2) == '(%x^%y)^2'

    assert str(sin(x)) == 'sin(%x)'
    assert str(3 * sin(x + y)) == '3*sin(%x+%y)'


def test_contained_parameters():
    x = Parameter('x')
    assert _contained_parameters(x) == {x}

    y = Parameter('y')
    assert _contained_parameters(x + y) == {x, y}

    assert _contained_parameters(x ** y ** sin(x * y * 4)) == {x, y}
