use <CRSPGR022.scad>
$fn = 30;

module square_cavity_array(x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions)
{
    /*  Formating */
    x_spacing = x_spacing + 0.00001;
    y_spacing = y_spacing + 0.00001;
    
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
    /*  Formating */
    x_spacing = x_spacing + 0.00001;
    y_spacing = y_spacing + 0.00001;
   
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

module GEARX0005_BG(modul, tooth_number, partial_cone_angle, tooth_width, bore, pressure_angle, helix_angle, x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions, cavity_type)
{
    difference()
    {
        

        CRSPGR022_BG(modul, tooth_number, partial_cone_angle, tooth_width, bore, pressure_angle, helix_angle);

        if (cavity_type == "S")
        {        
            translate([0,0,tooth_width / 2 + tooth_width])
            {
                square_cavity_array(x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions*2);
            }
        }
        else if (cavity_type == "C")
        {
            translate([0,0,tooth_width / 2 + tooth_width])
            {
                circular_cavity_array(x_spacing, y_spacing, x_units, y_units, x_offset, y_offset, x_cavity_dimensions, y_cavity_dimensions, z_cavity_dimensions*2);
            }
        }
        else
        {
            
        }
        

    }
}
    
module GEARX0005_MR()
{
    difference()
    {

        BOLTX0004_R();

    }
}
    
module GEARX0005_HR()
{
    difference()
    {

        BOLTX0004_R();

    }
}
    
module GEARX0005_MHR()
{
    difference()
    {

        BOLTX0004_R();

    }
}
    
module GEARX0005_SG()
{
    difference()
    {

        BOLTX0004_R();

    }
}
    
module GEARX0005_HG()
{
    difference()
    {

        BOLTX0004_R();

    }
}
    
module GEARX0005_RG()
{
    difference()
    {

        BOLTX0004_R();

    }
}
    
module GEARX0005_HRG()
{
    difference()
    {

        BOLTX0004_R();

    }
}
    
module GEARX0005_PG()
{
    difference()
    {

        BOLTX0004_R();

    }
}
    

module GEARX0005_BHG()
{
    difference()
    {

        BOLTX0004_R();

    }
}
    
module GEARX0005_W()
{
    difference()
    {

        GEARX0005_R();

    }
}



GEARX0005_BG(modul = 5, tooth_number = 32, partial_cone_angle = 45, tooth_width = 25, bore = 17.1, pressure_angle = 20, helix_angle = 0, x_spacing = (2*17.25^2)^0.5, y_spacing = (2*17.25^2)^0.5, x_units = 4, y_units = 4, x_offset = 0, y_offset = 0, x_cavity_dimensions = 7, y_cavity_dimensions = 7, z_cavity_dimensions = 50, cavity_type = "C");