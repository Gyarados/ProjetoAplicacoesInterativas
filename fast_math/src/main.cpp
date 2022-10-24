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

__declspec(dllexport) Coord __cdecl get_coords(float translation_x,
	float translation_y,
	float translation_z, 
	float rotation_right_z, 
	float rotation_up_z,
	float h_ref, 
	float v_ref, 
	float h_density, 
	float v_density) {
	
	float delta_x, delta_y;
	float new_x, new_y;

	delta_x = tan(rotation_right_z * PI) * translation_z;
	delta_y = tan(rotation_up_z * PI) * translation_z;

	new_x = h_ref - (translation_x + S * delta_x) * h_density;
	new_y = v_ref - (translation_y + S * delta_y) * v_density;

	return {new_x, new_y};
}