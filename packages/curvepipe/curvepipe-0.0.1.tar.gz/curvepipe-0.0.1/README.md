# Curve Pipe

CurvePipe is a curve-processing package designed to efficiently manipulate sets of curves without using dataframes or arrays.

With CurvePipe you can transform curves in a readable pipe-like syntax, which makes it not only suitable for python-beginners. Curve Pipe is perfect for professional engineers that want to write efficient scripts in a few lines of code that are maintainable and do not require a lot of documentation.


## Example
The following command scales the x vector by 2, adds an offset of 20 to the x vector and computes the logarithm for each value in the y vector.

```python
cpipe = CurvePipe(x=[0, 0.1, 0.2, 0.3, 0.4], y=[1, 2, 3, 3, 4])\
    .scale_x(2)\
    .offset_x(20.1) \
    .transform_y(lambda v: math.log(v))
```
