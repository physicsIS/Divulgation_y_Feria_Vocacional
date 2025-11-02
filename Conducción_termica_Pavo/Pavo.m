% Proyecto Metodo Numericos II 
% Por: 
%   Gabriel Alvarez Castrillo C00368
%
%
%
% Titulo: Escoger un titulo
% ¡El Pavo al Horno Perfecto: Cocinando con Algoritmos y Mucho Sazón!
% ¡Script y Sazón! La Guía Definitiva para Asar un Pavo
% Pavo Automático: Horneado a Prueba de Bugs
% Código al Horno: El Arte de Programar un Pavo Perfecto
%{
               .--.
              /} p \             /}
             `~)-) /           /` }
              ( / /          /`}.' }
               / / .-'""-.  / ' }-'}
              / (.'       \/ '.'}_.}
             |            `}   .}._}
             |     .-=-';   } ' }_.}
             \    `.-=-;'  } '.}.-}
              '.   -=-'    ;,}._.}
                `-,_  __.'` '-._}
                    `|||
                   .=='=,
%}
clearvars;
%Se carga la geometria stl
gm = fegeometry('ModeloPavo.stl');
figure(1)
pdegplot(gm, FaceLabels="off",EdgeLabels="off",FaceAlpha=0.5);
%........... Se crea el modelo...................
model = createpde();
importGeometry(model,'ModeloPavo.stl');%en milimetros
%Se ingresan los coeficientes del problema
% En este caso, ocupamos la difusividad termica de la carne de res
%alpha = 0.14e-6; % en m^2/s
alpha = 0.14; % en mm^2/s
specifyCoefficients(model, 'm',0,'d',1,'c',alpha,'a',0,'f',0, 'Cell', 1);

%Se aplican las condiciones de Dirichlet
T = 300; %C en la panza del pavo
applyBoundaryCondition(model,"dirichlet","Face",4,"r",T,"h",1);
%Se aplica Neumann
applyBoundaryCondition(model,"neumann","Face",1:3,"g",0,"q",0);
applyBoundaryCondition(model,"neumann","Face",5:28,"g",0,"q",0);

T_inicial = 20; %C
setInitialConditions(model,T_inicial);
%........ Se crea la malla.....
mesh = generateMesh(model,Hmax=25);
%Se grafica la malla
figure(2)
pdemesh(mesh,"FaceAlpha",0.2);


t = (0 : 100 : 20000);

%Ahora resolvemos el sistema
R = solvepde(model,t);
U = R.NodalSolution;
for i=1:size(t,2)
    figure(3)
    
    pdeplot3D(mesh, "ColorMapData",R.NodalSolution(:,i),"FaceAlpha",0.7)
    axis equal
    xlabel('x(m)')
    ylabel('y(m)')
    zlabel('z(m)')
    clim([0,300])
    string = ['t = ', num2str(t(i)), ' s'];
    title(string)
    %view(2)
    pause(1e-3) %mejorar velocidad animación
    
end

%---------Punto dentro del pavo-----------------
% Coordenadas del punto dentro del pavo
x_pto = 5;  % Coordenada en x (mm)
y_pto = 0;  % Coordenada en y (mm)
z_pto = 15;  % Coordenada en z (mm)

% Encuentra el nodo más cercano al punto deseado
distancia = sqrt((mesh.Nodes(1, :) - x_pto).^2 + ...
                 (mesh.Nodes(2, :) - y_pto).^2 + ...
                 (mesh.Nodes(3, :) - z_pto).^2);

[~, nodo_idx] = min(distancia);  

% Extrae la temperatura en ese nodo para todos los tiempos
temp_punto = U(nodo_idx, :);

% Gráfica de la temperatura del punto
figure(5);
plot(t, temp_punto, 'LineWidth', 2);
xlabel('Tiempo (s)');
ylabel('Temperatura (°C)');
title(['Variación de temperatura en el punto (', ...
       num2str(x_pto), ', ', num2str(y_pto), ', ', num2str(z_pto), ') mm']);
grid on;

%---------Promedio de Planos-----------------

% Rango de planos en z (en mm)
z_min = 0; 
z_max = 30;

% Inicialización del promedio de temperatura total
temp_promedio_total = zeros(1, length(t));

% Contador de planos procesados
num_planes = 0;

% Iteramos sobre los valores de z en pasos de 1mm
for z_plane = z_min:1:z_max
    % Seleccionamos los nodos en el plano actual
    mask = abs(mesh.Nodes(3, :) - z_plane) < 1; % Nodos cercanos al plano

    % Verificamos si hay nodos en este plano
    if any(mask)
        % Extraemos los valores de temperatura en este plano
        temp_section = U(mask, :);

        % Acumulamos el promedio del plano al total
        temp_promedio_total = temp_promedio_total + mean(temp_section, 1);

        % Contamos el número de planos procesados
        num_planes = num_planes + 1;
    end
end

% Calculamos el promedio final dividiendo entre el número de planos
temp_promedio_final = temp_promedio_total / num_planes;

% Graficamos la temperatura promedio acumulada a lo largo de z en función del tiempo
figure(6);
plot(t, temp_promedio_final, 'LineWidth', 2);
xlabel('Tiempo (s)');
ylabel('Temperatura Promedio (°C)');
title(['Temperatura promedio desde z = ', num2str(z_min), ' mm hasta z = ', num2str(z_max), ' mm']);
grid on;




