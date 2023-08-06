subroutine percent_true(percent, output)
    implicit none
    double precision, intent(in) :: percent
    logical, intent(out) :: output
    double precision :: result
    call canonical(result)
    output = result * 100 < percent
end subroutine percent_true

subroutine random_below(limit, output)
    implicit none
    integer, intent(in) :: limit
    integer, intent(out) :: output
    double precision :: result
    call canonical(result)
    if (limit > 0) then
        output = floor(limit * result)
    elseif (limit < 0) then
        output = -floor(-limit * result)
    else
        output = 0
    end if
end subroutine random_below

subroutine random_integer(low, high, output)
    implicit none
    integer, intent(in) :: low, high
    integer, intent(out) :: output
    integer :: result
    call random_below(1 + high - low, result)
    output = result + low
end subroutine random_integer

subroutine random_range(start, stop, step, output)
    implicit none
    integer, intent(in) :: start, stop, step
    integer, intent(out) :: output
    integer :: width, pivot, step_size, result
    if (start == stop .or. step == 0) then
        output = start
    else
        width = ABS(start - stop) - 1
        if (step > 0) then
            pivot = MIN(start, stop)
        else
            pivot = MAX(start, stop)
        end if
        step_size = ABS(step)
        call random_below((width + step_size) / step, result)
        output = pivot + step_size * result
    end if
end subroutine random_range

subroutine d(sides, output)
    implicit none
    integer, intent(in) :: sides
    integer, intent(out) :: output
    call random_integer(1, sides, output)
end subroutine d

subroutine dice(rolls, sides, output)
    implicit none
    integer, intent(in) :: rolls, sides
    integer, intent(out) :: output
    integer :: n, result
    do n = 1, rolls
        call d(sides, result)
        output = output + result
    end do
end subroutine dice

subroutine plus_or_minus(amount, output)
    implicit none
    integer, intent(in) :: amount
    integer, intent(out) :: output
    integer :: num
    num = ABS(amount)
    call random_integer(-num, num, output)
end subroutine plus_or_minus

subroutine plus_or_minus_linear(amount, output)
    implicit none
    integer, intent(in) :: amount
    integer, intent(out) :: output
    integer :: num
    num = ABS(amount)
    call dice(2, num + 1, output)
    output = output - (num + 2)
end subroutine plus_or_minus_linear

subroutine canonical(output)
    implicit none
    double precision, intent(out) :: output
    call random_number(output)
end subroutine canonical

subroutine random_float(low, high, output)
    implicit none
    double precision, intent(in) :: low, high
    double precision, intent(out) :: output
    double precision :: result
    call random_number(result)
    output = low + (result * (high - low))
end subroutine random_float

subroutine triangular(low, high, mode, output)
    implicit none
    double precision, intent(in) :: low, high, mode
    double precision, intent(out) :: output
    double precision :: rand, mode_factor
    if (low == high) then
        output = low
        return
    endif
    call canonical(rand)
    mode_factor = (mode - low) / (high - low)
    if (rand > mode_factor) then
        output = high + (low - high) * SQRT((1.0 - rand) * (1.0 - mode_factor))
    else
        output = low + (high - low) * SQRT(rand * mode_factor)
    end if
end subroutine triangular

subroutine random_index(limit, output)
    implicit none
    integer, intent(in) :: limit
    integer, intent(out) :: output
    if (limit > 0) then
        call random_below(limit, output)
    else
        call random_below(limit, output)
        output = output - 1
    end if
end subroutine random_index

subroutine front_linear(limit, output)
    implicit none
    integer, intent(in) :: limit
    integer, intent(out) :: output
    double precision :: real_limit
    double precision :: result
    real_limit = limit
    if (limit > 0) then
        call triangular(0.0d0, real_limit, 0.0d0, result)
    elseif (limit < 0) then
        call triangular(real_limit, 0.0d0, real_limit, result)
    else
        result = 0.0
    end if
    output = FLOOR(result)
end subroutine front_linear

subroutine back_linear(limit, output)
    implicit none
    integer, intent(in) :: limit
    integer, intent(out) :: output
    double precision :: real_limit
    double precision :: result
    real_limit = limit
    if (limit > 0) then
        call triangular(0.0d0, real_limit, real_limit, result)
    elseif (limit < 0) then
        call triangular(real_limit, 0.0d0, 0.0d0, result)
    else
        result = 0.0
    end if
    output = FLOOR(result)
end subroutine back_linear

subroutine middle_linear(limit, output)
    implicit none
    integer, intent(in) :: limit
    integer, intent(out) :: output
    double precision :: real_limit
    double precision :: result
    real_limit = limit
    if (limit > 0) then
        call triangular(0.0d0, real_limit, real_limit / 2, result)
    elseif (limit < 0) then
        call triangular(real_limit, 0.0d0, real_limit / 2, result)
    else
        result = 0.0
    end if
    output = FLOOR(result)
end subroutine middle_linear

subroutine quantum_linear(limit, output)
    implicit none
    integer, intent(in) :: limit
    integer, intent(out) :: output
    integer :: result
    call d(3, result)
    if (result == 1) then
        call front_linear(limit, output)
    elseif (result == 2) then
        call middle_linear(limit, output)
    else
        call back_linear(limit, output)
    end if
end subroutine quantum_linear
