from jft.text_colours.bright.magenta import f as mg
from jft.text_colours.bright.cyan import f as cy
from jft.pf import f as pf

f = lambda u, v: None if u == v else (
  [{'u_i': u[i], 'v_i': v[i], 'i': i} for i in range(len(u)) if u[i] != v[i]][0]
  if len(u) == len(v) else (
    {'u_i': None, 'v_i': v[len(u)], 'i': len(u)} if len(u) < len(v)
    else {'u_i': u[len(v)], 'v_i': None, 'i': len(v)}
  )
)

def t_diff_strs_same_length():
  x_u = 'abcde'
  x_v = 'abxde'
  y = {'u_i': 'c', 'v_i': 'x', 'i': 2}
  z = f(x_u, x_v)
  return y == z or pf(['y != z', f'y: {y}', f'z: {z}' ])

def t_matching_strs():
  x_u = 'abcde'
  x_v = 'abcde'
  y = None
  z = f(x_u, x_v)
  return y == z or pf(['y != z', f'y: {y}', f'z: {z}' ])

def t_diff_strs_u_len_lt_v_len():
  x_u = 'abcd'
  x_v = 'abcdxfg'
  y = {'u_i': None, 'v_i': 'x', 'i': 4}
  z = f(x_u, x_v)
  return y == z or pf(['y != z', f'y: {y}', f'z: {z}' ])

def t_diff_strs_u_len_gt_v_len():
  x_u = 'abcdxfg'
  x_v = 'abcd'
  y = {'u_i': 'x', 'v_i': None, 'i': 4}
  z = f(x_u, x_v)
  return y == z or pf(['y != z', f'y: {y}', f'z: {z}' ])

def t():
  if not t_diff_strs_same_length(): return pf('!t_diff_strs_same_length')
  if not t_matching_strs(): return pf('!t_matching_strs')
  if not t_diff_strs_u_len_lt_v_len(): return pf('!t_diff_strs_u_len_lt_v_len')
  if not t_diff_strs_u_len_gt_v_len(): return pf('!t_diff_strs_u_len_gt_v_len')
  return True
