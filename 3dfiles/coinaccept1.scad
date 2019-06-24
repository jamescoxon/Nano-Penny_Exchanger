
front_x = 50;
front_y = 10;
front_z = 70;

screw_hole_r = 0.9;

device_gap_x = 20;
device_gap_z = 50;

difference() {
	cube([front_x,front_y,front_z], true);

	cube([device_gap_x,15,device_gap_z], true);
    
	//Screw top left
	translate([20,0,20]) rotate ([90,0,0]) cylinder (h = (front_y + 5), r=screw_hole_r, center = true, $fn=100);
	//Screw bottom left
	translate([-20,0,20]) rotate ([90,0,0]) cylinder (h = (front_y + 5), r=screw_hole_r, center = true, $fn=100);
	//Screw bottom right
	translate([-20,0,-20]) rotate ([90,0,0]) cylinder (h = (front_y + 5), r=screw_hole_r, center = true, $fn=100);
	//Screw Top right
	translate([20,0,-20]) rotate ([90,0,0]) cylinder (h = (front_y + 5), r=screw_hole_r, center = true, $fn=100);

}