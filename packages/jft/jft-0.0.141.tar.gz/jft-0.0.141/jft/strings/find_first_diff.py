from jft.text_colours.bright.magenta import f as mg
from jft.text_colours.bright.cyan import f as cy
from jft.pf import f as pf

f = lambda u, v: [
  {'u_i': u[i], 'v_i': v[i], 'i': i}
  for i in range(min([len(_) for _ in [u, v]]))
  if u[i] != v[i]
][0] if u!=v else None

def t_different_strings():
  x_u = 'abcde'
  x_v = 'abxde'
  y = {'u_i': 'c', 'v_i': 'x', 'i': 2}
  z = f(x_u, x_v)
  return y == z or pf(['y != z', f'y: {y}', f'z: {z}' ])


def t_matching_strings():
  x_u = 'abcde'
  x_v = 'abcde'
  y = None
  z = f(x_u, x_v)
  return y == z or pf(['y != z', f'y: {y}', f'z: {z}' ])

def t():
  if not t_different_strings(): return pf('not t_0')
  if not t_matching_strings(): return pf('not t_matching_strings')
  return True
