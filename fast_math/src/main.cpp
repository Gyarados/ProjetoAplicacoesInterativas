#include <iostream>
#include <math.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define S 0.1
#define PI 3.14159265358979323846

struct Coord {
	float x;
	float y;
};

Coord get_coords(int argc, char *argv[]) {
	
	float translation_x = atof(argv[1]); 
	float translation_y = atof(argv[2]); 
	float translation_z = atof(argv[3]); 
	float rotation_right_z = atof(argv[4]); 
	float rotation_up_z = atof(argv[5]);
	float h_ref = atof(argv[6]); 
	float v_ref = atof(argv[7]); 
	float h_density = atof(argv[8]); 
	float v_density = atof(argv[9]);

	float delta_x, delta_y;
	float new_x, new_y;

	delta_x = tan(rotation_right_z * PI) * translation_z;
	delta_y = tan(rotation_up_z * PI) * translation_z;

	new_x = h_ref - (translation_x + S * delta_x) * h_density;
	new_y = v_ref - (translation_y + S * delta_y) * v_density;

	return {new_x, new_y};
}