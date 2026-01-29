import sympy as sp

(
L_1xx, L_1xy, L_1xz, L_1yy, L_1yz, L_1zz,
L_2xx, L_2xy, L_2xz, L_2yy, L_2yz, L_2zz,
L_3xx, L_3xy, L_3xz, L_3yy, L_3yz, L_3zz,
L_4xx, L_4xy, L_4xz, L_4yy, L_4yz, L_4zz,
L_5xx, L_5xy, L_5xz, L_5yy, L_5yz, L_5zz,
L_6xx, L_6xy, L_6xz, L_6yy, L_6yz, L_6zz,
l_1x, l_1y, l_1z,
l_2x, l_2y, l_2z,
l_3x, l_3y, l_3z,
l_4x, l_4y, l_4z,
l_5x, l_5y, l_5z,
l_6x, l_6y, l_6z,
m_1, m_2, m_3, m_4, m_5, m_6,
fv_1, fv_2, fv_3, fv_4, fv_5, fv_6,
fc_1, fc_2, fc_3, fc_4, fc_5, fc_6
) = sp.symbols('''
L_1xx L_1xy L_1xz L_1yy L_1yz L_1zz
L_2xx L_2xy L_2xz L_2yy L_2yz L_2zz
L_3xx L_3xy L_3xz L_3yy L_3yz L_3zz
L_4xx L_4xy L_4xz L_4yy L_4yz L_4zz
L_5xx L_5xy L_5xz L_5yy L_5yz L_5zz
L_6xx L_6xy L_6xz L_6yy L_6yz L_6zz
l_1x l_1y l_1z
l_2x l_2y l_2z
l_3x l_3y l_3z
l_4x l_4y l_4z
l_5x l_5y l_5z
l_6x l_6y l_6z
m_1 m_2 m_3 m_4 m_5 m_6
fv_1 fv_2 fv_3 fv_4 fv_5 fv_6
fc_1 fc_2 fc_3 fc_4 fc_5 fc_6
''')

θ_b = []
θ_b[0] = L_1yy + L_2yy + L_3zz + 13*l_1x/25 + 169*m_1/2500 - 987*m_2/2500 - 15841*m_3/40000 - 15841*m_4/40000 - 15841*m_5/40000 - 15841*m_6/40000
θ_b[1] = fv_1
θ_b[2] = fc_1
θ_b[3] = L_2xx - L_2yy + 289*m_2/625 + 289*m_3/625 + 289*m_4/625 + 289*m_5/625 + 289*m_6/625
θ_b[4] = L_2xy
θ_b[5] = L_2xz - 17*l_2z/25 + 17*l_3y/25
θ_b[6] = L_2yz
θ_b[7] = L_2zz - 289*m_2/625 - 289*m_3/625 - 289*m_4/625 - 289*m_5/625 - 289*m_6/625
θ_b[8] = l_2x + 17*m_2/25 + 17*m_3/25 + 17*m_4/25 + 17*m_5/25 + 17*m_6/25
θ_b[9] = l_2y
θ_b[10] = fv_2
θ_b[11] = fc_2
θ_b[12] = L_3xx - L_3zz + L_4zz + 97*l_4y/50 + 49*m_3/40000 + 7537*m_4/8000 + 7537*m_5/8000 + 7537*m_6/8000
θ_b[13] = L_3xy + 7*l_3y/200
θ_b[14] = L_3xz
θ_b[15] = L_3yy + L_4zz + 97*l_4y/50 - 49*m_3/40000 + 37587*m_4/40000 + 37587*m_5/40000 + 37587*m_6/40000
θ_b[16] = L_3yz
θ_b[17] = l_3x - 7*m_3/200 - 7*m_4/200 - 7*m_5/200 - 7*m_6/200
θ_b[18] = l_3z + l_4y + 97*m_4/100 + 97*m_5/100 + 97*m_6/100
θ_b[19] = fv_3
θ_b[20] = fc_3
θ_b[21] = L_4xx - L_4zz + L_5zz
θ_b[22] = L_4xy
θ_b[23] = L_4xz
θ_b[24] = L_4yy + L_5zz
θ_b[25] = L_4yz
θ_b[26] = l_4x
θ_b[27] = l_4z - l_5y
θ_b[28] = fv_4
θ_b[29] = fc_4
θ_b[30] = L_5xx - L_5zz + L_6yy + 23*l_6z/100 + 529*m_6/40000
θ_b[31] = L_5xy
θ_b[32] = L_5xz
θ_b[33] = L_5yy + L_6yy + 23*l_6z/100 + 529*m_6/40000
θ_b[34] = L_5yz
θ_b[35] = l_5x
θ_b[36] = l_5z + l_6z + 23*m_6/200
θ_b[37] = fv_5
θ_b[38] = fc_5
θ_b[39] = L_6xx - L_6yy
θ_b[40] = L_6xy
θ_b[41] = L_6xz
θ_b[42] = L_6yz
θ_b[43] = L_6zz
θ_b[44] = l_6x
θ_b[45] = l_6y
θ_b[46] = fv_6
θ_b[47] = fc_6