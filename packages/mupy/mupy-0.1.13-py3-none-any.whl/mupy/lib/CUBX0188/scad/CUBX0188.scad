$fn = 50;

module general_block(block_length, shaft_radius )
{

    difference()
    {
        cube([block_length, block_length, block_length],true);

        rotate([0,0,0]) { cylinder( h = block_length+0.1, r1 = shaft_radius, r2 = shaft_radius, center = true ); }
        rotate([90,0,0]) { cylinder( h = block_length+0.1, r1 = shaft_radius, r2 =shaft_radius, center = true ); }
        rotate([0,90,0]){ cylinder( h = block_length+0.1, r1 = shaft_radius, r2 = shaft_radius, center = true ); }
        rotate([0,90,0]) { cylinder( h = block_length+0.1, r1 = shaft_radius, r2 = shaft_radius, center = true ); }
    
        
    }
}

module advanced_side_tooth(block_length, shaft_radius, padding )
{
    cubic_corner_to_edge_angle = 54.7;
    //corner_cropping_constant = 0.5722 * block_length;
    corner_cropping_constant = 0.49 * block_length;
    edge_cropping_constant = 0.77;
    
    difference()
    {
        cube([block_length-padding, block_length, block_length],true);
        rotate([0,0,0]) { cylinder( h = block_length+0.1, r1 = shaft_radius, r2 = shaft_radius, center = true ); }
        rotate([90,0,0]) { cylinder( h = block_length+0.1, r1 = shaft_radius, r2 =shaft_radius, center = true ); }
        rotate([0,90,0]){ cylinder( h = block_length+0.1, r1 = shaft_radius, r2 = shaft_radius, center = true ); }
        rotate([0,90,0]) { cylinder( h = block_length+0.1, r1 = shaft_radius, r2 = shaft_radius, center = true ); }
        translate([corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,45])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,135])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,315])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }       
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,225])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,45])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
            
        }
        translate([-corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,135])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,315])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,225])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        
        translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        
        rotate([90,0,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
        rotate([0,90,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
    }
}



module advanced_block(block_length, shaft_radius)
{

    cubic_corner_to_edge_angle = 54.7;
    //corner_cropping_constant = 0.5722 * block_length;
    corner_cropping_constant = 0.49 * block_length;
    edge_cropping_constant = 0.77;
    difference()
    {
        general_block(block_length,shaft_radius);
        
        translate([corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,45])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,135])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,315])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }       
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,225])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,45])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
            
        }
        translate([-corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,135])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,315])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,225])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        
        translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        
        rotate([90,0,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
        rotate([0,90,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
    }

}


module advanced_tooth_coupling_block(block_length, shaft_radius)
{

    cubic_corner_to_edge_angle = 54.7;
    //corner_cropping_constant = 0.5722 * block_length;
    corner_cropping_constant = 0.59 * block_length;
    edge_cropping_constant = 0.77;
    difference()
    {
        general_block(block_length,shaft_radius);
        
        translate([corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,45])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,135])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,315])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }       
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,225])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,45])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
            
        }
        translate([-corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,135])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,315])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,225])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        
        translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        
        rotate([90,0,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
        rotate([0,90,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
    }

}



module advanced_perimeter_block(block_length, shaft_radius)
{

    cubic_corner_to_edge_angle = 54.7;
    //corner_cropping_constant = 0.5722 * block_length;
    corner_cropping_constant = 0.49 * block_length;
    edge_cropping_constant = 0.77;
    difference()
    {
        general_block(block_length,shaft_radius);
        
        translate([corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,45])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,135])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,315])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }       
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,225])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,45])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
            
        }
        translate([-corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,135])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,315])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,225])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        
        translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        
        rotate([90,0,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
        rotate([0,90,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
    }

}

module advanced_corner_block(block_length, shaft_radius)
{

    cubic_corner_to_edge_angle = 54.7;
    //corner_cropping_constant = 0.5722 * block_length;
    corner_cropping_constant = 0.59 * block_length;
    edge_cropping_constant = 0.77;
    

    
    difference()
    {
        general_block(block_length,shaft_radius);
        
        translate([corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,45])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,135])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,315])
            {
                //FIX
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }       
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,225])
            {
                //FIX
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,45])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
            
        }
        translate([-corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,135])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,315])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,225])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        
        translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        
        rotate([90,0,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                  cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
        rotate([0,90,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //THIS
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //THIS
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
    }

}


module advanced_top_tooth(block_length, shaft_radius, padding = 0.2)
{
    cubic_corner_to_edge_angle = 54.7;
    //corner_cropping_constant = 0.5722 * block_length;
    corner_cropping_constant = 0.49 * block_length;
    edge_cropping_constant = 0.77;
    
    difference()
    {
        cube([block_length-padding, block_length-padding, block_length],true);
        rotate([0,0,0]) { cylinder( h = block_length+0.1, r1 = shaft_radius, r2 = shaft_radius, center = true ); }
        rotate([90,0,0]) { cylinder( h = block_length+0.1, r1 = shaft_radius, r2 =shaft_radius, center = true ); }
        rotate([0,90,0]){ cylinder( h = block_length+0.1, r1 = shaft_radius, r2 = shaft_radius, center = true ); }
        rotate([0,90,0]) { cylinder( h = block_length+0.1, r1 = shaft_radius, r2 = shaft_radius, center = true ); }
        translate([corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,45])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,135])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,54.7,315])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }       
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,corner_cropping_constant])
        {
            rotate([0,54.7,225])
            {
                cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,45])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
            
        }
        translate([-corner_cropping_constant,corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,135])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            //54.7 is an essential angle. This is the cut blockl
            rotate([0,-54.7,315])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        translate([-corner_cropping_constant,-corner_cropping_constant,-corner_cropping_constant])
        {
            rotate([0,-54.7,225])
            {
                //cube([block_length/2.0, block_length/2.0, block_length/2],true);
            }
        }
        
        translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
        {
            rotate([0,0,45])
            {
                cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
            }
        }
        
        rotate([90,0,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
        rotate([0,90,0])
        {
            translate([block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            
            translate([-block_length*edge_cropping_constant,block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    //cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
            translate([-block_length*edge_cropping_constant,-block_length*edge_cropping_constant,0])
            {
                rotate([0,0,45])
                {
                    cube([block_length+0.01, block_length+0.01, block_length+0.01],true);
                }
            }
        }
        
    }
}
    
module square_cavity_array(x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions)
{
    /*  Constants */
    x_length = ( x_units - 1 ) * x_spacing;
    y_length = ( y_units - 1 ) * y_spacing;
    
    /* Main grid building loop. */
    for ( x_step = [ - x_length / 2 : x_spacing : x_length / 2 ])
    {
        /* Main grid building loop. */
        for ( y_step = [ - y_length / 2 : y_spacing : y_length / 2 ])
        {
            translate([x_step + x_offset, y_step + y_offset, 0 ]) { rotate([0,0,0]) { cube([x_cavity_dimensions,y_cavity_dimensions,z_cavity_dimensions], center = true); } }
        }
    }
}

module circular_cavity_array(x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions)
{
    /*  Constants */
    x_length = ( x_units - 1 ) * x_spacing;
    y_length = ( y_units - 1 ) * y_spacing;
    
    /* Main grid building loop. */
    for ( x_step = [ - x_length / 2 : x_spacing : x_length / 2 ])
    {
        /* Main grid building loop. */
        for ( y_step = [ - y_length / 2 : y_spacing : y_length / 2 ])
        {
            translate([x_step + x_offset, y_step + y_offset, 0 ]) { rotate([0,0,0]) { scale([x_cavity_dimensions,y_cavity_dimensions,1]) {cylinder(h=z_cavity_dimensions, r1=1/2, r2=1/2, center=true); } } }
        }
    }
}



module CUBX0188_BPAN(block_length, shaft_radius, xunits, yunits, padding = 0.2, side_teeth_orientation = "regular", top_teeth_included = true, x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions, cavity_type)
{
    echo(x_units);
    difference()
    {
        union()
        {
            /*  Constants */
            xlength = ( xunits - 3 ) * block_length;
            ylength = ( yunits - 3 ) * block_length;
            inner_cavity_block_thickness = block_length;
            top_teeth_block_thickness = block_length;
            
            /* Main grid building loop. */
            for ( x_step = [ - xlength / 2 : block_length : xlength / 2 ])
            {
                /* Main grid building loop. */
                for ( y_step = [ - ylength / 2 : block_length : ylength / 2 ])
                {
                    /* If printing outer perimeter ( Not including teeth ) . */
                    if (y_step == ylength / 2 || y_step == - ylength / 2 || x_step == xlength / 2 || x_step == - xlength / 2)
                    {
                        
                        /* Non-Corner Perimeter Blocks*/
                        
                        if ( y_step == ylength / 2 && abs(x_step) != xlength / 2  ) 
                        {  
                            translate([x_step,y_step, 0 ]) 
                            { 
                                rotate([0,0,90]) 
                                { 
                                    if (xunits%2==1 && side_teeth_orientation == "regular") 
                                    { 
                                        if (xunits%4==3)
                                        {
                                            if ((x_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                            else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        }
                                        if (xunits%4==1)
                                        {
                                            if ((x_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                            else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                        }
                                    }
                                    if (xunits%2==0 && side_teeth_orientation == "regular") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (xunits%2==0 && side_teeth_orientation == "inverted") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (xunits%2==1 && side_teeth_orientation == "inverted") 
                                    { 
                                       if ((x_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                    if (xunits%2==1 && side_teeth_orientation == "chimera") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (xunits%2==0 && side_teeth_orientation == "chimera") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                    if (xunits%2==1 && side_teeth_orientation == "inverted_chimera") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (xunits%2==0 && side_teeth_orientation == "inverted_chimera") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                } 
                            } 
                        }



                        if ( y_step == - ylength / 2 && abs(x_step) != xlength / 2) 
                        {  
                            translate([x_step,y_step, 0 ]) 
                            { 
                                rotate([0,0,-90]) 
                                {  
                                    if (xunits%2==1 && side_teeth_orientation == "regular") 
                                    { 
                                        if (xunits%4==3)
                                        {
                                            
                                            if ((x_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                            else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                        }
                                        if (xunits%4==1)
                                        {
                                            if ((x_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                            else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                        }
                                    }
                                    if (xunits%2==0 && side_teeth_orientation == "regular") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (xunits%2==0 && side_teeth_orientation == "inverted") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (xunits%2==1 && side_teeth_orientation == "inverted") 
                                    { 
                                       if ((x_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                    if (xunits%2==1 && side_teeth_orientation == "chimera") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (xunits%2==0 && side_teeth_orientation == "chimera") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                    if (xunits%2==1 && side_teeth_orientation == "inverted_chimera") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (xunits%2==0 && side_teeth_orientation == "inverted_chimera") 
                                    { 
                                        if ((x_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                } 
                            } 
                        }
                        if ( x_step == xlength / 2 && abs(y_step) != ylength / 2) 
                        { 
                            translate([x_step,y_step, 0 ]) 
                            { 
                                rotate([0,0,0]) 
                                { 
                                    if (y_units%2==1 && side_teeth_orientation == "regular") 
                                    { 
                                        if (yunits%4==3)
                                        {
                                            
                                            if ((y_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                            else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                        }
                                        if (yunits%4==1)
                                        {
                                            if ((y_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                            if ((y_step+block_length/2)%(2*block_length)==block_length) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        }
                                        
                                    }
                                    if (yunits%2==0 && side_teeth_orientation == "regular") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (yunits%2==0 && side_teeth_orientation == "inverted") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (yunits%2==1 && side_teeth_orientation == "inverted") 
                                    { 
                                       if ((y_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                    if (yunits%2==1 && side_teeth_orientation == "chimera") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (yunits%2==0 && side_teeth_orientation == "chimera") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                    if (yunits%2==1 && side_teeth_orientation == "inverted_chimera") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (yunits%2==0 && side_teeth_orientation == "inverted_chimera") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                } 
                            } 
                        }
                        if ( x_step == - xlength / 2 && abs(y_step) != ylength / 2 )
                        { 
                            translate([x_step,y_step, 0 ]) 
                            { 
                                rotate([0,0,180]) 
                                { 
                                    if (yunits%2==1 && side_teeth_orientation == "regular") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (yunits%2==0 && side_teeth_orientation == "regular") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (yunits%2==0 && side_teeth_orientation == "inverted") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (yunits%2==1 && side_teeth_orientation == "inverted") 
                                    { 
                                       if ((y_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                    if (yunits%2==1 && side_teeth_orientation == "chimera") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (yunits%2==0 && side_teeth_orientation == "chimera") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                    if (yunits%2==1 && side_teeth_orientation == "inverted_chimera") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    }
                                    if (yunits%2==0 && side_teeth_orientation == "inverted_chimera") 
                                    { 
                                        if ((y_step+block_length/2)%(2*block_length)==0) { color("red") {advanced_tooth_coupling_block(block_length + 0.001, shaft_radius ); } } 
                                        else { color("green") {advanced_perimeter_block(block_length + 0.001, shaft_radius ); } }
                                    } 
                                } 
                            } 
                        }
                        
                        /* Corner Blocks */
                        
                        
                        if ( x_step == xlength / 2 && y_step == ylength / 2 ) 
                        { 
                            translate([x_step,y_step, 0 ]) 
                            { 
                                rotate([0,0,0]) 
                                { 
                                    advanced_corner_block(block_length + 0.001, shaft_radius ); 
                                } 
                            } 
                        }
                        
                        if ( x_step ==  xlength / 2 && y_step == - ylength / 2 ) 
                        { 
                            translate([x_step,y_step, 0 ]) 
                            { 
                                rotate([0,0,270]) 
                                {
                                    advanced_corner_block(block_length + 0.001, shaft_radius ); 
                                } 
                            } 
                        }
                        if ( x_step == - xlength / 2 && y_step == ylength / 2 ) 
                        { 
                            translate([x_step,y_step, 0 ]) 
                            { 
                                rotate([0,0,90]) 
                                {
                                    advanced_corner_block(block_length + 0.001, shaft_radius ); 
                                } 
                            } 
                        }
                        if ( x_step == - xlength / 2 && y_step == - ylength / 2 ) 
                        { 
                            translate([x_step,y_step, 0 ]) 
                            { 
                                rotate([0,0,180]) 
                                { 
                                    advanced_corner_block(block_length + 0.001, shaft_radius ); 
                                } 
                            } 
                        }
                    }
                    
                    
                    /* If printing inner cavity. */
                    else if ( y_step <= abs(ylength / 2 - block_length) || x_step <= abs(xlength / 2 - block_length ) ) 
                    { 
                        translate([ x_step,y_step, - ( block_length - inner_cavity_block_thickness ) / 2 ] ) 
                        { 
                            general_block(block_length + 0.001, shaft_radius );
                        
                        } 
                    }
                }
            }
            
            /*  Side Teeth  */
            if ( side_teeth_orientation == "regular" )
            {
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ]) { if ( (x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == block_length ) { translate([x_tooth_step , ylength / 2 + block_length , 0 ]) { advanced_side_tooth( block_length + 0.001, shaft_radius, padding ); } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( (y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == 0 ) { translate([xlength / 2 + block_length , y_tooth_step , 0 ]) { rotate([0,0,270]) {advanced_side_tooth( block_length + 0.001, shaft_radius, padding ); } } } }
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ]) { if ( (x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == 0 ) { translate([x_tooth_step , -ylength / 2 - block_length , 0 ]) { rotate([0,0,180]) { advanced_side_tooth( block_length + 0.001, shaft_radius, padding );} } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( (y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == block_length ) { translate([-xlength / 2 - block_length , y_tooth_step , 0 ]) { rotate([0,0,90]) { advanced_side_tooth( block_length + 0.001, shaft_radius, padding );} } } }
            }
            else if ( side_teeth_orientation == "inverted" )
            {
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ]) { if ( (x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == 0 ) { translate([x_tooth_step , ylength / 2 + block_length , 0 ]) { advanced_side_tooth(block_length + 0.001, shaft_radius, padding ); } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( (y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == block_length ) { translate([xlength / 2 + block_length , y_tooth_step , 0 ]) { rotate([0,0,270]) { advanced_side_tooth(block_length + 0.001, shaft_radius, padding ); } } } }
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ]) { if ( (x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == block_length ) { translate([x_tooth_step , -ylength / 2 - block_length , 0 ]) { rotate([0,0,180]) { advanced_side_tooth( block_length + 0.001, shaft_radius, padding ); } } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( (y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == 0 ) { translate([-xlength / 2 - block_length , y_tooth_step , 0 ]) { rotate([0,0,90]) { advanced_side_tooth(block_length + 0.001, shaft_radius, padding ); } } } }
            }
            else if ( side_teeth_orientation == "chimera" )
            {
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ]) { if ( (x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == block_length ) { translate([x_tooth_step , ylength / 2 + block_length , 0 ]) { advanced_side_tooth(block_length + 0.001, shaft_radius, padding ); } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( (y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == 0 ) { translate([xlength / 2 + block_length , y_tooth_step , 0 ]) { rotate([0,0,270]) { advanced_side_tooth(block_length + 0.001, shaft_radius, padding ); } } } }
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ]) { if ( (x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == block_length ) { translate([x_tooth_step , -ylength / 2 - block_length , 0 ]) { rotate([0,0,180]) { advanced_side_tooth( block_length + 0.001, shaft_radius, padding ); } } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( (y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == 0 ) { translate([-xlength / 2 - block_length , y_tooth_step , 0 ]) { rotate([0,0,90]) { advanced_side_tooth(block_length + 0.001, shaft_radius, padding ); } } } }
            }
            else if ( side_teeth_orientation == "inverted_chimera" )
            {
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ]) { if ( (x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == 0 ) { translate([x_tooth_step , ylength / 2 + block_length , 0 ]) { advanced_side_tooth(block_length + 0.001, shaft_radius, padding ); } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( (y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == block_length ) { translate([xlength / 2 + block_length , y_tooth_step , 0 ]) { rotate([0,0,270]) { advanced_side_tooth(block_length + 0.001, shaft_radius, padding ); } } } }
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ]) { if ( (x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == 0 ) { translate([x_tooth_step , -ylength / 2 - block_length , 0 ]) { rotate([0,0,180]) { advanced_side_tooth( block_length + 0.001, shaft_radius, padding ); } } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( (y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == block_length ) { translate([-xlength / 2 - block_length , y_tooth_step , 0 ]) { rotate([0,0,90]) { advanced_side_tooth(block_length + 0.001, shaft_radius, padding ); } } } }
            }
            else
            {
                
            }

            /*  Top Teeth  */
            if (top_teeth_included == true)
            {

                /*  Top Teeth  */
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ]) { if ( (x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == block_length && !(x_tooth_step == xlength / 2 ) && !(x_tooth_step == -xlength / 2 )) { translate([x_tooth_step , ylength / 2 , block_length - ( block_length - top_teeth_block_thickness ) / 2 ]) { if (!( x_tooth_step == xlength / 2 ) && !( x_tooth_step == - xlength / 2 ) ) { advanced_top_tooth(block_length+ 0.001, shaft_radius, padding); } } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( ( y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == 0 && ! ( y_tooth_step == ylength / 2 ) && ! ( y_tooth_step == - ylength / 2 ) ) { translate([xlength / 2 , y_tooth_step , block_length - ( block_length - top_teeth_block_thickness ) / 2  ]) { if (!( y_tooth_step == ylength / 2 ) && !( y_tooth_step == - ylength / 2 ) )  {  advanced_top_tooth(block_length+ 0.001, shaft_radius, padding);  } } } }
                for ( x_tooth_step = [ - xlength / 2 : block_length : xlength / 2 ] ) { if ( ( x_tooth_step + xlength / 2 ) % ( block_length * 2 )  == 0 && ! ( x_tooth_step == xlength / 2 ) && ! ( x_tooth_step == -xlength / 2 ) ) { translate([x_tooth_step , - ylength / 2 , block_length - ( block_length - top_teeth_block_thickness ) / 2  ] ) { if (!( x_tooth_step == xlength / 2 ) && !( x_tooth_step == - xlength / 2 ) ) { advanced_top_tooth(block_length+ 0.001, shaft_radius, padding);  } } } }
                for ( y_tooth_step = [ - ylength / 2 : block_length : ylength / 2 ]) { if ( ( y_tooth_step + ylength / 2 ) % ( block_length * 2 )  == block_length && ! ( y_tooth_step == ylength / 2 ) && ! ( y_tooth_step == - ylength / 2 ) ) { translate([ - xlength / 2 , y_tooth_step , block_length - ( block_length - top_teeth_block_thickness ) / 2  ]) { if (!( y_tooth_step == ylength / 2 ) && !( y_tooth_step == - ylength / 2 ) ) { advanced_top_tooth(block_length+ 0.001, shaft_radius, padding); } } } }
            }
        }
        
        if (cavity_type == "S")
        {        
            translate([0,0,block_length / 2])
            {
                square_cavity_array(x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions*2);
            }
        }
        else if (cavity_type == "C")
        {
            translate([0,0,block_length / 2])
            {
                circular_cavity_array(x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions*2);
            }
        }
        else
        {
            
        }
    }
}

module CUBX0188_SPAN(block_length, shaft_radius, xunits, yunits, x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions, cavity_type)
{
    difference()
    {
        union()
        {
            /*  Constants */
            xlength = ( xunits - 1 ) * block_length;
            ylength = ( yunits - 1 ) * block_length;

            /* Main grid building loop. */
            for ( x_step = [ - xlength / 2 : block_length : xlength / 2 ])
            {
                /* Main grid building loop. */
                for ( y_step = [ - ylength / 2 : block_length : ylength / 2 ])
                {
                    translate([ x_step,y_step, 0 ] ) 
                    { 
                        general_block(block_length + 0.001, shaft_radius );
                    }  
                }
            }

        }
        
        if (cavity_type == "S")
        {        
            translate([0,0,block_length / 2])
            {
                square_cavity_array(x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions*2);
            }
        }
        else if (cavity_type == "C")
        {
            translate([0,0,block_length / 2])
            {
                circular_cavity_array(x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions*2);
            }
        }
        else
        {
            
        }
    }
}


/* Axle Adapter */
module CUBX0188_AXAD( block_length, shaft_radius, padding )
{
    difference()
    {
        union()
        {
            translate([block_length*0, block_length*0, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*1, block_length*0, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*1, block_length*-1, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-1, block_length*-1, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-1, block_length*1, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-1, block_length*0, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*0, block_length*-1, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*0, block_length*1, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*1, block_length*1, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }

            translate([block_length*1, block_length*0, block_length*1]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*1, block_length*-1, block_length*1]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-1, block_length*-1, block_length*1]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-1, block_length*1, block_length*1]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-1, block_length*0, block_length*1]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*0, block_length*-1, block_length*1]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*0, block_length*1, block_length*1]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*1, block_length*1, block_length*1]) { general_block(block_length + 0.01, shaft_radius ); }

            translate([block_length*1, block_length*0, block_length*2]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*1, block_length*-1, block_length*2]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-1, block_length*-1, block_length*2]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-1, block_length*1, block_length*2]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-1, block_length*0, block_length*2]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*0, block_length*-1, block_length*2]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*0, block_length*1, block_length*2]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*1, block_length*1, block_length*2]) { general_block(block_length + 0.01, shaft_radius ); }
            
            translate([block_length*2, block_length*0, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*0, block_length*-2, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*-2, block_length*0, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }
            translate([block_length*0, block_length*2, block_length*0]) { general_block(block_length + 0.01, shaft_radius ); }

        }
        translate([0,0,block_length*1]) { cube([block_length+padding, block_length+padding, block_length+padding],true);}
        translate([0,0,block_length*2]) { cube([block_length+padding, block_length+padding, block_length+padding],true);}
        
    }
}


/* Axle - Flywheel Adapter */
module CUBX0188_FYAD( block_length, shaft_radius )
{
    translate([0*block_length, 0*block_length, 0*block_length]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*1, block_length*0, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*1, block_length*-1, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*-1, block_length*-1, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*-1, block_length*1, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*-1, block_length*0, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*0, block_length*-1, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*0, block_length*1, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*1, block_length*1, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    
    translate([block_length*2, block_length*0, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*2, block_length*0, block_length*1]) { advanced_block(block_length + 0.01, shaft_radius ); }

    translate([block_length*0, block_length*-2, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*0, block_length*-2, block_length*1]) { advanced_block(block_length + 0.01, shaft_radius ); }

    translate([block_length*-2, block_length*0, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*-2, block_length*0, block_length*1]) { advanced_block(block_length + 0.01, shaft_radius ); }
    
    translate([block_length*0, block_length*2, block_length*0]) { advanced_block(block_length + 0.01, shaft_radius ); }
    translate([block_length*0, block_length*2, block_length*1]) { advanced_block(block_length + 0.01, shaft_radius ); }
}

/* Axle - Flywheel Adapter */
module CUBX0188_AXLE( block_length, shaft_radius, axle_blocks )
{
    length = block_length*(axle_blocks-1);
    for ( x_block_step = [ - length / 2 : block_length : length / 2 ]) 
    { 
        translate([x_block_step,0,0])
        {
            scale([1.0001,1,1])
            {
                general_block(block_length, shaft_radius);
            }
        }
    }
}


CUBX0188_BPAN(block_length=7.5, shaft_radius=2.25, xunits=10, yunits=8, padding = 0.0, side_teeth_orientation = "inverted_chimera", top_teeth_included = true, x_spacing=10, y_spacing=10, x_units=1, y_units=1, x_offset=0, y_offset=0, x_cavity_dimensions=10, y_cavity_dimensions=10, z_cavity_dimensions=0, cavity_type="C");

//advanced_side_tooth(10, 2.5, 0.2 );
//CUBX0188_FYAD( 25, 5 );
//advanced_perimeter_block()

//advanced_corner_block( 25, 5 );

//advanced_block(10,2.5);
