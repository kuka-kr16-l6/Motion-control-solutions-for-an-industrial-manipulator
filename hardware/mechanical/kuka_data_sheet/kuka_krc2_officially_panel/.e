
*   CONFIGURATION

default_config	dont_care			;
use_config	dont_use			;
config_family	cf_over_head_pos		; 
joint_config_family j3	joint_cf_elbow_up	;
joint_default_config j3	dont_care		;
joint_config_family j5	joint_cf_pos		;
joint_default_config j5	dont_care		;

*   TURNS

* Changes for axis 1 +/- 185 deg
* Volker Miegel Dec 1997
default_turns j1 0 0.0, j4 0 0.0, j6 0 0.0;
joint_default_turn  all 0;
joint_default_turn  j1 5;

*   ZONES
*   FINE		

zone_define fine no_smooth;		

*   MEDIUM		

*   $APO.CPTP = 3 		
*   Only realistic if angles > 6 deg		
zone_joint_type medium	dist	;
zone_joints_param medium	0.052 0.052 0.052 0.052 0.052 0.052	;

*  $APO.CDIS = 20 		
*  Only realistic if distance > 40 mm		
zone_type medium	dist	;
zone_cart_param medium	20	;

*  COARSE		

*  $APO.CPTP = 9 		
*  Only realistic if angles > 18 degrees		
zone_joint_type coarse	dist	;
zone_joints_param coarse	0.157 0.157 0.157 0.157 0.157 0.157	;

*  $APO.CDIS = 50 mm		
*  Only realistic if distance > 100 mm		
zone_type coarse	dist	;
zone_cart_param coarse	50	;

*  NODECEL		

*  PTP: workaround to emulate way smaller than $APO.CPTP/2		
zone_joint_type nodecel	speed	;
zone_joints_param nodecel	99.0 99.0 99.0 99.0 99.0 99.0	;

*  $APO.CVEL 99% 		
*  (workaround to emulate way smaller than $APO.CDIS/2)		
zone_type nodecel	speed	;
zone_cart_param nodecel	99	;

