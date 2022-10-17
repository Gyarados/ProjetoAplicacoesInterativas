#include <math.h>

#define S 0.1
#define PI 3.14159265358979323846

__declspec(dllexport) float __cdecl get_coord(
	int h_or_v,
	float translation_x_or_y, 
	float translation_z, 
	float rotation_right_or_up_z, 
	float h_or_v_ref, 
	float h_or_v_density) {

	// x, right e h = 1
	// y, up e v = 0

	float delta;
	float new_coord;

	delta = tan(rotation_right_or_up_z * PI) * translation_z;

	if (h_or_v == 1) {
		new_coord = h_or_v_ref - (translation_x_or_y + S * delta) * h_or_v_density;
	} else {
		new_coord = h_or_v_ref + (translation_x_or_y - S * delta) * h_or_v_density;
	}
	
	return new_coord;
}