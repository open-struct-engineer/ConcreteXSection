
def constant_stress_block(segments, stress):
    """
    A function to calculate P,Mx, and My by line
    integral along given line segments for a constant
    stress

    Parameters
    ----------
    segments: List of two tuples/lists of two floats
                each segment should be of the form [[x1,y1],[x2,y2]]
                each x,y should be a float
                example input:
                [[[x11,y11][x21,y21]],...,[[x1i,y1i],[x2i,y2i]]]

    stress: float
            constant stress value for region

    Returns:
    ---------
    P: float
        Sum of Axial force from all segments
    Mx: float
        Sum of Moments about the x-axis from all segments
    My: float
        Sum of Moments about the y-axis from all segments
    x: float
        x centroid coordinate of P action
    y: float
        y centroid coordinate of P action
    details: list of floats
            list of P,Mx,My values per segment
    """

    f = stress
    P = 0
    Mx = 0
    My = 0
    x = 0
    y = 0
    details = []

    for s in segments:
        x1 = s[0][0]
        y1 = s[0][1]
        x2 = s[1][0]
        y2 = s[1][1]

        axial = -1*0.5*f*(x1+x2)*(y1-y2)
        P += axial

        momentx = (1/6.0)*f*(y2-y1)*((x1*((2*y1)+y2))+(x2*(y1+(2*y2))))
        Mx += momentx

        momenty = (1/6.0)*f*((x1*x1)+(x1*x2)+(x2*x2))*(y2-y1)
        My += momenty

        details.append([axial,momentx,momenty])

    x = My/P
    y = Mx/P

    return P,Mx,My,[x,y],details

def linear_stress_block(segments, q1, q1_y, q2, q2_y):
    """
    A function to calculate P,Mx, and My by line
    integral along given line segments for a linearly
    varing stress distribution

    Parameters
    ----------
    segments: List of two tuples/lists of two floats
                each segment should be of the form [[x1,y1],[x2,y2]]
                each x,y should be a float. y1 or y2 should exactly match
                q1_y or q2_y.
                example input:
                [[[x11,y11][x21,y21]],...,[[x1i,y1i],[x2i,y2i]]]

    q1: float
        stress value 1 for region, usually the start stress
    q1_y: float
        y-coordinate/elevation where q1 applies,
        used to swap q1 and q2 when needed.
    q2: float
        stress value 2 for region, usually the end stress
    q2_y: float
        y-coordinate/elevation where q2 applies,
        used to swap q1 and q2 when needed.

    Returns:
    ---------
    P: float
        Sum of Axial force from all segments
    Mx: float
        Sum of Moments about the x-axis from all segments
    My: float
        Sum of Moments about the y-axis from all segments
    x: float
        x centroid coordinate of P action
    y: float
        y centroid coordinate of P action
    details: list of floats
            list of P,Mx,My values per segment
    """
    f = stress
    P = 0
    Mx = 0
    My = 0
    x = 0
    y = 0
    details = []

    for s in segments:
        x1 = s[0][0]
        y1 = s[0][1]
        x2 = s[1][0]
        y2 = s[1][1]

        # set start and end stress based on y coordinate of segment end point
        if y2 == q2_y:
            qs = q1
            qe = q2
        else:
            qs = q2
            qe = q1

        axial = (1/6.0)*(y2-y1)*((qs*((2*x1)+x2))+(qe*(x1+(2*x2))))
        P += axial

        momentx = ((1/12.0)*(y2-y1)
                    * (
                        qs*x1*((3*y1)+y2)
                        + qs*x2*(y1+y2)
                        + qe*x1*(y1+y2)
                        + qe*x2*(y1+(3*y2))
                        )
                    )
        Mx += momentx

        momenty = ((-1/24.0)*(y1-y2)
                    * (
                        x1*x1*((3*qs)+qe)
                        + 2*x1*x2*(qs+qe)
                        + x2*x2*(qs+(3*qe))
                        )
                    )
        My += momenty

        details.append([axial,momentx,momenty])

    x = My/P
    y = Mx/P

    return P,Mx,My,[x,y],details

def ec2_parabolic_stress_block(segments, fcd, n, eu, ec2, c, yna):
    """
    A function to calculate P,Mx, and My by line
    integral along given line segments for a linearly
    varing stress distribution

    Parameters
    ----------
    segments: List of two tuples/lists of two floats
                each segment should be of the form [[x1,y1],[x2,y2]]
                each x,y should be a float. y1 or y2 should exactly match
                the y-coordinte associated with ec2 or the neutral axis y,na.
                example input:
                [[[x11,y11][x21,y21]],...,[[x1i,y1i],[x2i,y2i]]]

    fcd: float
            design peak stress see EN 1992.1.1.2004
    n: float
        parabolic formula exponent see EN 1992.1.1.2004 table 3.1
    eu: float
        ultimate strain see EN 1992.1.1.2004 table 3.1
    ec2: float
        strain limit for parabolic region of stress-strain see EN 1992.1.1.2004 table 3.1
    c: float
        depth of the neutral axis as measured from the peak y coordinate of the cross section
    yna: float
        y coordinate/elevation of the neutral axis

    Returns:
    ---------
    P: float
        Sum of Axial force from all segments
    Mx: float
        Sum of Moments about the x-axis from all segments
    My: float
        Sum of Moments about the y-axis from all segments
    x: float
        x centroid coordinate of P action
    y: float
        y centroid coordinate of P action
    details: list of floats
            list of P,Mx,My values per segment

    Notes:
    -------
    Bounds of integration for P,Mx, and My are from Y,na to Y,ec2 only
    Once in the constant stress region use the integral formulations for
    a constant stress, this includes any edge segments with a constant Y
    this should eliminate any chance for div/0 errors with the below formulas

    formuala for strain:
    ec = C1x + C2y + C3 base assumption 1: section rotated so strain only varies in y
    ec = C2y + C3

    y = y,na -- ec = 0
    0 = C2 y,na + C3
    C3 = -C2 y,na

    y = y,max -- ec = eu
    eu = C2 y,max + C3
    eu = C2 y,max - C2 y,na
    eu = C2 (y,max - y,na)--> na depth = c
    eu = C2 c
    C2 = eu/c

    ec = (eu/c)y - (eu/c) y,na
    ec = (eu/c)*(y-y,na)

    EC2 Parabolic Formula in interval 0<= ec <= ec2:
    stress = fcd [1-(1-(ec/ec2))^n]

    Substitute in ec
    stress = fcd [1-(1-((eu*(y-y,na))/(c*ec2)))^n] --> define k = eu/ec2
    stress = fcd [1-(1-((k*y - k*y,na)/c))^n]

    Assumption 2: Cross section is defined by linear segments defined by (x,y)
               counter-clockwise ordered coord. pairs and and translated such
               that the point about which we want to sum moments is located at
               (0,0). Cross section first and last coordinate are the same and
               the segments form a regular closed polygon.

    Assumption 2 means the edge is a closed piecewise curve which allows the use
    of Green's Theorem to formulate a line integral for the enclosed volume.

    dbl integral F(x,y) da = dbl integral (dQ/dx + dP/dy) = integral P dx + Q dy

    for an arbitrary line segment defined by two coordinates (x1,y1) and (x2,y2)
    parametric formulas for the line are:
    x(t) = x1 + t(x2-x1) and dx = (x2-x1) dt
    y(t) = y1 + t(y2-y1) and dy = (y2-y1) dt

    --- Axial - P: ---
    Basic formula for P = dbl integral stress(x,y) dA
    Per above stress only varies in y which makes choosing P and Q easier

    Try P = 0 and Q = x * stress(y)
    dP/dy = 0 and dQ/dx = stress(y)
    dP/dy - dQ/x = stress(y), so the chosen substitution should work

    integral x*stress(y) dy
    substitution of the parametric formulas yields
    integral (x1 + t(x2-x1))*(fcd [1-(1-((k*(y1+t(y2-y1)) - k*y,na)/c))^n])*(y2-y1)dt
    range of the integral now becomes 0 to 1

    Wolfram-Alpha Input for P
    (to avoid problems with subscripts and constants variables have been replaced per
    the above input comments)
    integrate[(A+t*(B-A))*(F*(1-(1-(((K*(D+t*(E-D)))-(K*Y))/C))^N))*(E-D),t]
    (formulas below are the indefinite integral, ran into computation time issues
    so need to evaluate at t=0 and t=1 and subtract results)

    --- Moment about the Y-Axis - My: ---
    Basic formula for My = dbl integral x*stress(x,y) dA
    Per above stress only varies in y which makes choosing P and Q easier

    Try P = 0 and Q = 1/2 * x^2 * stress(y)
    dP/dy = 0 and dQ/dx = x * stress(y)
    dP/dy - dQ/x = x * stress(y), so the chosen substitution should work

    integral 1/2*x^2*stress(y) dy
    substitution of the parametric formulas yields
    integral (1/2)*(x1 + t(x2-x1))^2*(fcd [1-(1-((k*(y1+t(y2-y1)) - k*y,na)/c))^n])*(y2-y1)dt
    range of the integral now becomes 0 to 1

    Wolfram-Alpha Input for My
    Integrate[(1/2) (A + t (B - A))^2 (F (1 - (1 - (K (D + t (E - D)) - K Y)/C)^N)) (E - D), t]

    Note Because of how Wolfram-Alpha chooses to simplify the results the above integral
    results in a term that contains (.../(B-A)) which if x1 = x2 would result in a div/0
    error. Solving a second integral for the case when x1 = x2 was done and an if statement
    used below to capture that case.

    Wolfram-Alpha Input for My when x1=x2
    Integrate[(1/2) (A + t (A - A))^2 (F (1 - (1 - (K (D + t (E - D)) - K Y)/C)^N)) (E - D), t]

    --- Moment about the X-Axis - x: ---
    Basic formula for My = dbl integral y*stress(x,y) dA
    Per above stress only varies in y which makes choosing P and Q easier

    Try P = 0 and Q = y * x * stress(y)
    dP/dy = 0 and dQ/dx = y * stress(y)
    dP/dy - dQ/x = y * stress(y), so the chosen substitution should work

    integral y*x*stress(y) dy
    substitution of the parametric formulas yields
    integral (y1 + t(y2-y1))*(x1 + t(x2-x1))*(fcd [1-(1-((k*(y1+t(y2-y1)) - k*y,na)/c))^n])*(y2-y1)dt
    range of the integral now becomes 0 to 1

    Wolfram-Alpha Input for Mx
    Integrate[(D + t (E - D)) (A + t (B - A)) (F (1 - (1 - (K (D + t (E - D)) - K Y)/C)^N)) (E - D), t]
    """

    P = 0
    Mx = 0
    My = 0
    x = 0
    y = 0
    details = []


    F = fcd     # Fcd
    K = eu/ec2  # eu/ec2
    N = n       # n from table 3.1
    C = c       # NA Depth = Y,max - Y,na
    Y = yna     # Y,na = actual Y-coordinate of neutral Axis


    for s in segments:
        A = s[0][0] # X1
        B = s[1][0] # X2
        D = s[0][1] # Y1 = Y,na
        E = s[1][1] # Y2 = Y coordinate that corresponds to ec2

        # If y1 > y2 then on a decending segment so switch x1,y1
        # to match direction of integration
        if D > E:
            A = s[1][0] # X1
            B = s[0][0] # X2
            D = s[1][1] # Y1 = Y coordinate that corresponds to ec2
            E = s[0][1] # Y2 = Y,na

        axial = []
        for t in range(0,2):

            Pintegral = ((-1*D + E)*
                    F*(
                        A*t + (((-1*A + B)*t*t)*0.5)
                        - (
                            (C + K*(D*(-1 + t) - E*t + Y))
                            *(math.pow((1 + (K*(D*(-1 + t) - E*t + Y))/C),N))
                            *(
                                A*(C + K*(-1*(D*(1 + N)*(-1 + t)) + E*(-2 + N*(-1 + t) + t) + Y))
                                - B*(C + K*(E*(1 + N)*t - D*(1 + t + N*t) + Y))
                            )
                        )
                        /((D - E)*(D-E)*K*K*(1 + N)*(2 + N))
                    )
                    )

            axial.append(Pintegral)

        P += (axial[1]-axial[0])

        momenty = []

        for t in range(0,2):

            if A==B:
                My_integral = (
                                (
                                    A*A*(D - E)*F
                                    * (
                                        -1*t
                                        + (
                                            (C + K*(D*(-1 + t) - E*t + Y))
                                            * math.pow((1 + (K*(D*(-1 + t) - E*t + Y))/C),N)
                                            )
                                            /((D - E)*K*(1 + N))
                                        )
                                    )/2.0)
            else:
                My_integral = (
                                -1*(
                                    (D - E)*F
                                    * (
                                        math.pow((A*(-1 + t) - B*t),3)
                                        - (
                                            3*math.pow((1 + (K*(D*(-1 + t) - E*t + Y))/C),N)
                                            * (
                                                math.pow((D - E),3)
                                                * K*K*K*(1 + N)*(2 + N)
                                                * math.pow((A*(-1 + t) - B*t),3)
                                                - math.pow((D - E),2)
                                                * K*K*N*(1 + N)
                                                * math.pow((A*(-1 + t) - B*t),2)
                                                * (B*(C + K*(-D + Y)) - A*(C + K*(-E + Y)))
                                                - 2*(D - E)*K*N*(A*(-1 + t) - B*t)
                                                * math.pow((B*(C + K*(-D + Y)) - A*(C + K*(-E + Y))),2)
                                                - 2
                                                * math.pow((B*(C + K*(-D + Y)) - A*(C + K*(-E + Y))),3)
                                                )
                                            )
                                            / (
                                                math.pow((D - E),3)*K*K*K*(1 + N)*(2 + N)*(3 + N)
                                                )
                                        )
                                    )
                                    / (6.0*(A - B))
                                )

            momenty.append(My_integral)

        My  += (momenty[1]-momenty[0])

        momentx = []

        for t in range(0,2):

            Mx_integral = (
                            (-1.0*D + E)
                            * F
                            * (
                                A*D*t
                                + (((B*D + A*(-2.0*D + E))*t*t)*0.5)
                                + (((A - B)*(D - E)*t*t*t)/3.0)
                                - (
                                    math.pow((1 + (K*(D*(-1 + t) - E*t + Y))/C),N)
                                    * (
                                        (A - B)
                                        * math.pow((D - E),3)
                                        * math.pow(K,3)*(1 + N)*(2 + N)*t*t*t
                                        + math.pow((D - E),2)*K*K*(1 + N)*t*t
                                        * (
                                            -3.0*A*D*K*(2 + N)
                                            + A*E*K*(3 + N)
                                            + B*D*K*(3 + 2*N)
                                            + A*N*(C + K*Y)
                                            - B*N*(C + K*Y)
                                            )
                                        - (C + K*(-D + Y))
                                        * (
                                            B*(C + K*(-D + Y))
                                            * (2*C + K*(D + D*N + 2*Y))
                                            - A
                                            * (
                                                2*C*C
                                                + C*K*(2*D*(1 + N) - E*(3 + N) + 4*Y)
                                                + K*K*(
                                                        D*D*(2 + 3*N + N*N)
                                                        - D*(1 + N)*(E*(3 + N) - 2*Y)
                                                        + Y*(-(E*(3 + N)) + 2*Y)
                                                        )
                                                )
                                            )
                                        + (D - E)*K*t
                                        * (
                                            B*N*(C + K*(-D + Y))*(2*C + K*(D + D*N + 2*Y))
                                            + A
                                            * (
                                                3*D*D*K*K*(2 + 3*N + N*N)
                                                + N*(-2*C + E*K*(3 + N) - 2*K*Y)
                                                * (C + K*Y)
                                                - 2*D*K*(1 + N)*(E*K*(3 + N) + N*(C + K*Y))
                                                )
                                            )
                                        )
                                    )
                                    / (math.pow((D - E),2)*K*K*K*(1 + N)*(2 + N)*(3 + N))
                                )
                            )

            momentx.append(Mx_integral)

        Mx += (momentx[1]-momentx[0])

        details.append([(axial[1]-axial[0]),(momentx[1]-momentx[0]),(momenty[1]-momenty[0])])

    x = My/P
    y = Mx/P

    return P,Mx,My,[x,y],details
