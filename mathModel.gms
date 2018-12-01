Sets
i Compliance /Csa, Csv, Cpa, Cpv/
alias(j,i);

Scalar Rs  Resistencia vascular para los vasos sanguineos sistemicos /17.5/
          Rp  Resistencia vascular para los vasos sanguineos pulmonares /1.79/
          Kr   Coeficiente de bombeo de sangre para el lado derecho del corazón /2.8/
          Kl   Coeficiente de bombeo de sangre para el lado izquierdo del corazón /1.12/
          Vo   Volemia /5/ ;

*Grafica de volumen contra valores de complianzas, bombeo - patologias

Parameter T(i) Valores T;

T('Csa') = 1/Kr+Rs;
T('Csv') = 1/Kr;
T('Cpa') = 1/Kl + Rp;
T('Cpv') = 1/Kl;

Variables
x(i)    Compliance i
z       minimize;

Positive Variable x;

Equations
objFunc     Función Objetivo
V               Restricción de los volumenes
P               Restricción de las presiones
total          Restricción suma de los volumenes
pos(i)         Restricción positivo
;

objFunc .. sum(i, T(i)*x(i))*z =e= Vo;

V(i) .. T(i)*x(i)*Vo =g= 0.0001*sum(j, T(j)*x(j));

P(i) .. T(i)*x(i)*Vo =g= 0.0001*sum(j, T(j)*x(j))*x(i);

total .. sum(i, T(i)*x(i)*Vo) =e= Vo*sum(j, T(j)*x(j));

pos(i) .. x(i)*T(i) =g= 0.000001;

Model Model1 /all/ ;
option nlp=CONOPT

Solve Model1 using nlp minimizing z ;

Display z.l
Display x.l