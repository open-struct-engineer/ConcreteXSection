'''
BSD 3-Clause License
Copyright (c) 2020, open-struct-engineer developers
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from geometry import ConcreteSection
 
x = [0,12,12,84,84,-16,-16,0,0]
y = [0,0,16,16,24,24,16,16,0]
 
material = 5000
Section = ConcreteSection.ConcreteSection(x, y, material)

segments = Section.define_segments()

alpha = 2.0853
x_t = 6
y_t = 12

xp,yp = Section.transformed_vertices_radians(x_t, y_t, alpha)

rt_segments = [[[xp[i[0]],yp[j[0]]],[xp[i[0]+1],yp[j[0]+1]]] for i,j in zip(enumerate(xp[1:]),enumerate(yp[1:]))]

y_whitney = 6.931244
f_c1 = 4.25
f_c2 = f_c1
p = []
mx = []
my = []

# Below will be basis for Whitney Block Function on concrete or void section

for edge in rt_segments:
    
    #Check if y greater than both ends of segment
    if y_whitney >= edge[0][1] and y_whitney >= edge[1][1]:
        pass
    
    # Case of a horizontal edge
    elif edge[0][1] == edge[1][1]:
        
        x1 = edge[0][0]
        y1 = edge[0][1]
        x2 = edge[1][0]
        y2 = edge[1][1]
        
        pe = (1/6.0)*(y2-y1)*((f_c1*((2*x1)+x2))+(f_c2*(x1+(2*x2))))
        mxe = ((1/12.0)
                *(y2-y1)
                    *(
                        (f_c1*x1*((3*y1)+y2))
                        + (f_c1*x2*(y1+y2))
                        + (f_c2*x1*(y1+y2))
                        + (f_c2*x2*(y1+(3*y2)))
                    )
                )
        mye = ((1/24.0)
               *(y1-y2)
               *(
                    (x1*x1*((3*f_c1)+f_c2))
                    + (2*x1*x2*(f_c1+f_c2))
                    + (x2*x2*(f_c1+(3*f_c2)))
                )
               )
        
        p.append(pe)
        mx.append(mxe)
        my.append(mye)
                       
    # Case of entire edge above stress block boundary
    elif y_whitney <= edge[0][1] and y_whitney <= edge[1][1]:
        x1 = edge[0][0]
        y1 = edge[0][1]
        x2 = edge[1][0]
        y2 = edge[1][1]
        
        pe = (1/6.0)*(y2-y1)*((f_c1*((2*x1)+x2))+(f_c2*(x1+(2*x2))))
        mxe = ((1/12.0)
                *(y2-y1)
                    *(
                        (f_c1*x1*((3*y1)+y2))
                        + (f_c1*x2*(y1+y2))
                        + (f_c2*x1*(y1+y2))
                        + (f_c2*x2*(y1+(3*y2)))
                    )
                )
        mye = ((1/24.0)
               *(y1-y2)
               *(
                    (x1*x1*((3*f_c1)+f_c2))
                    + (2*x1*x2*(f_c1+f_c2))
                    + (x2*x2*(f_c1+(3*f_c2)))
                )
               )
        
        p.append(pe)
        mx.append(mxe)
        my.append(mye)
        
    else:
        
        # Compute Parametric t for stress block boundary
        # note strain only varies in y so only need to 
        # solve for t using y parametric formula
        
        t = (y_whitney - edge[0][1])/(edge[1][1]-edge[0][1])
        
        xt = edge[0][0] + (t*(edge[1][0]-edge[0][0]))
        yt = edge[0][1] + (t*(edge[1][1]-edge[0][1]))
        
        if edge[0][1] <= y_whitney:
            x1 = xt
            y1 = yt
            x2 = edge[1][0]
            y2 = edge[1][1]
            
            pe = (1/6.0)*(y2-y1)*((f_c1*((2*x1)+x2))+(f_c2*(x1+(2*x2))))
            mxe = ((1/12.0)
                    *(y2-y1)
                        *(
                            (f_c1*x1*((3*y1)+y2))
                            + (f_c1*x2*(y1+y2))
                            + (f_c2*x1*(y1+y2))
                            + (f_c2*x2*(y1+(3*y2)))
                        )
                    )
            mye = ((1/24.0)
                   *(y1-y2)
                   *(
                        (x1*x1*((3*f_c1)+f_c2))
                        + (2*x1*x2*(f_c1+f_c2))
                        + (x2*x2*(f_c1+(3*f_c2)))
                    )
                   )
            
            p.append(pe)
            mx.append(mxe)
            my.append(mye) 
        
        else:
            x1 = edge[0][0]
            y1 = edge[0][1]
            x2 = xt
            y2 = yt
            
            pe = (1/6.0)*(y2-y1)*((f_c1*((2*x1)+x2))+(f_c2*(x1+(2*x2))))
            mxe = ((1/12.0)
                    *(y2-y1)
                        *(
                            (f_c1*x1*((3*y1)+y2))
                            + (f_c1*x2*(y1+y2))
                            + (f_c2*x1*(y1+y2))
                            + (f_c2*x2*(y1+(3*y2)))
                        )
                    )
            mye = ((1/24.0)
                   *(y1-y2)
                   *(
                        (x1*x1*((3*f_c1)+f_c2))
                        + (2*x1*x2*(f_c1+f_c2))
                        + (x2*x2*(f_c1+(3*f_c2)))
                    )
                   )
            
            p.append(pe)
            mx.append(mxe)
            my.append(mye)

P = sum(p)
Mx = sum(mx)
My = sum(my)   

print(P)
print(Mx)
print(My)

