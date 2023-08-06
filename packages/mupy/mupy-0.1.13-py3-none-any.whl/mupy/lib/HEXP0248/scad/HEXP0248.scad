module HEXP0248_FOIL(foil_thickness, foil_radius, shaft_radius) 
{

    difference()
    {

        cylinder( h = foil_thickness, r1 = foil_radius, r2 = foil_radius, center = true, $fn = 6 );

        scale_factor = foil_radius/100;
        
        for ( i = [ 0 : 60 : 350 ])
        {
            rotate([0,0,i+30])
            { 
                translate([100*0.7 * scale_factor,0,0])
                { 
                    for ( j = [ -25.5 * scale_factor : 25.5 * scale_factor : 25.5 * scale_factor ])
                    {
                        for ( i = [ -25.5 * scale_factor : 25.5 * scale_factor : 25.5 * scale_factor ])
                        {
                            translate([j,i,0]) { rotate([0,0,0]) { cylinder( h = 50, r1 = shaft_radius, r2 = shaft_radius, center = true, $fn = 10 ); } }
                        }
                    }
                    
                    //cylinder( h = 50, r1 = 2, r2 = 2, center = true, $fn = 25 ); 

                } 
            }
        }
    }
}

HEXP0248_FOIL(foil_thickness = 0.5 , foil_radius = 80, shaft_radius = 2.2);