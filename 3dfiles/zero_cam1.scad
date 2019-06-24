
cam_x = 60;
cam_y = 12;
cam_z = 2;
screw_r = 1.1;
pi_gap = 23;

union(){
	cube([cam_x, cam_y, cam_z], true);
	translate([-(cam_x / 2) + 5,0,0]) cube([10, pi_gap + 4, cam_z], true);
	translate([-(cam_x / 2) + 5,(pi_gap/2),1.5]) rotate ([0,0,0]) cylinder (h = 5, r=screw_hole_r, center = true, $fn=100);
	translate([-(cam_x / 2) + 5,-(pi_gap/2),1.5]) rotate ([0,0,0]) cylinder (h = 5, r=screw_hole_r, center = true, $fn=100);
}

