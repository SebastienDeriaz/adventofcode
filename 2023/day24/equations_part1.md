
$$A : \begin{pmatrix}x\\y\end{pmatrix} = \begin{pmatrix}p_x\\p_y\end{pmatrix}+t\begin{pmatrix}v_x\\v_y\end{pmatrix}$$

$$B : \begin{pmatrix}x\\y\end{pmatrix} = \begin{pmatrix}p_x\\p_y\end{pmatrix}+t\begin{pmatrix}v_x\\v_y\end{pmatrix}$$


$$\begin{cases}
    x = p_{x_a} + tv_{x_a}\\
    y = p_{y_a} + tv_{y_a}\\
    x = p_{x_b} + tv_{x_b}
\end{cases}$$

$$\begin{cases}
    -v_{x_a}t_a + x = p_{x_a}\\
    -v_{y_a}t_a + y = p_{y_a}\\
    -v_{x_b}t_b + x = p_{x_b}\\
    -v_{y_b}t_b + y = p_{y_b}
\end{cases}$$

$$\begin{pmatrix}
1 & 0 & -v_{x_a} & 0\\
0 & 1 & -v_{y_a} & 0\\
1 & 0 & 0 & -v_{x_b}\\
0 & 1 & 0 & -v_{y_b}
\end{pmatrix}\begin{pmatrix}x\\y\\t_a\\t_b\end{pmatrix}=\begin{pmatrix}
p_{x_a}\\
p_{y_a}\\
p_{x_b}\\
p_{y_b}
\end{pmatrix}$$

$$\begin{pmatrix}x\\y\\t_a\\t_b\end{pmatrix}=\begin{pmatrix}
1 & 0 & -v_{x_a} & 0\\
0 & 1 & -v_{y_a} & 0\\
1 & 0 & 0 & -v_{x_b}\\
0 & 1 & 0 & -v_{y_b}
\end{pmatrix}^{-1}\begin{pmatrix}
p_{x_a}\\
p_{y_a}\\
p_{x_b}\\
p_{y_b}
\end{pmatrix}$$
