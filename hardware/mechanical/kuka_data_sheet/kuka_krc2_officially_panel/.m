##040003109504182400001
*
* Compile mechanism for kr16l6
*
begin COMPONENT kr16l6
	no_of_joints		6
	no_of_loops		0
	TCP_link_name		k7
	user_TCP :
0	0	1	1345	
0	1	0	0	
-1	0	0	1320	
0	0	0	1	
	inverse_family	-1
	base_name		k1

	begin LINK k2
		joint_from	k1
		transformation_to_father :
1	0	0	0	
0	1	0	0	
0	0	1	0	
0	0	0	1	
		joint_name	j1
		axis_points	0 0 200 , 0 0 0
		param_index	0
		joint_type	rot
		user_value	0
		range		-185 185
		max_speed	90
		max_acceleration	90
	end;

	begin LINK k3
		joint_from	k2
		transformation_to_father :
0	0	1	-415	
0	1	0	0	
-1	0	0	935	
0	0	0	1	
		joint_name	j2
		axis_points	260 -100 675 , 260 100 675
		param_index	1
		joint_type	rot
		user_value	0
		range		-155 35
		max_speed	90
		max_acceleration	90
	end;

	begin LINK k4
		joint_from	k3
		transformation_to_father :
0	0	-1	1615	
0	1	0	0	
1	0	0	1094.999512	
0	0	0	1	
		joint_name	j3
		axis_points	260 -100 1355 , 260 100 1355
		param_index	2
		joint_type	rot
		user_value	0
		range		-130 154
		max_speed	90
		max_acceleration	90
	end;

	begin LINK k5
		joint_from	k4
		transformation_to_father :
1	0	0	0	
0	1	0	0	
0	0	1	0	
0	0	0	1	
		joint_name	j4
		axis_points	800 0 1320 , 700 0 1320
		param_index	3
		joint_type	rot
		user_value	0
		range		-350 350
		max_speed	90
		max_acceleration	90
	end;

	begin LINK k6
		joint_from	k5
		transformation_to_father :
1	0	0	0	
0	1	0	0	
0	0	1	0	
0	0	0	1	
		joint_name	j5
		axis_points	1230 -75 1320 , 1230 75 1320
		param_index	4
		joint_type	rot
		user_value	0
		range		-130 130
		max_speed	90
		max_acceleration	90
	end;

	begin LINK k7
		joint_from	k6
		transformation_to_father :
1	0	0	0	
0	1	0	0	
0	0	1	0	
0	0	0	1	
		joint_name	j6
		axis_points	1345 0 1320 , 1230 0 1320
		param_index	5
		joint_type	rot
		user_value	0
		range		-350 350
		max_speed	90
		max_acceleration	90
	end

end
