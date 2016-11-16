/**
 * Created by Timo on 16.06.2014.
 * Modified by Frédéric P.A. Vogt, 09.2016; frederic.vogt@alumni.anu.edu.au 
 * (from an original fetched at http://examples.x3dom.org/clipPlane/clipplane.js)
 *    - Corrected updateProxy() to handle rotation+translation correctly.
 *    - Added the Distance() function to fetch the _distance from outside.
 *    - Added the Angle() function to fetch the _angle (in degrees) from the outside.
 *    - Added the State() function to toogle the transparency of the clipPlane.
 *    - Set the clip plane and proxy plane color to black.
 */
var ClipPlane = function ( scope, proxyParent, runtime )
{
    var _enabled = "true" // FPAV: added a variable tracking the "visibility"
    
    var _axis = "X";

    var _scope = scope;

    var _clipPlane = null;

    var _color = "0 0 0"; //FPAV: set color of the plane to black for aesthetic purposes.

    var _volume = null;

    var _clipping = -1;

    var _normal = new x3dom.fields.SFVec3f(_clipping, 0, 0);
    
    var _angle = 0;
    
    var _distance = 0;

    var _proxyTransform = null;
    
    var _proxyMat = null;

    var _proxyCoordinates = null;

    var _proxyParent = proxyParent;

    var _runtime = runtime;

    var initialize = function ()
    {
        updateVolume();
        createProxy();
        createClipPlane();
    };
    
    // FPAV: a function to grab the distance of the clip plane from the outside.
    this.Distance = function()
    {
        return Math.round(_distance*10)/10;    
    };
    
    // FPAV: a function to grab the angle of the clip plane from the outside.
    this.Angle = function()
    {
        return Math.round(180/3.14159265*_angle);
    };
    
    // The function dealing with translations
    this.Move = function ( value )
    {
        if ( _axis == "X" )
        {
            _distance = ((_volume.max.x - _volume.min.x) * value) + _volume.min.x;
        }
        else if ( _axis == "Y" )
        {
            _distance = ((_volume.max.y - _volume.min.y) * value) + _volume.min.y;
        }
        else if ( _axis == "Z" )
        {
            _distance = ((_volume.max.z - _volume.min.z) * value) + _volume.min.z;
        }

        updateClipPlane();
        updateProxy();
    };
    
    // The function dealing with the rotations.
    this.Rotate = function ( value )
    {
        var rotMat;
        
        _angle += value;

        if ( _axis == "X" )
        {
            // Convert the value to a rotation Matrix
            rotMat = x3dom.fields.SFMatrix4f.rotationY( value );

            // Rotate the normal
            _normal = rotMat.multMatrixPnt( _normal );
        }
        else if ( _axis == "Y" )
        {
            // Convert the value to a rotation Matrix
            rotMat = x3dom.fields.SFMatrix4f.rotationZ( value );

            // Rotate the normal
            _normal = rotMat.multMatrixPnt( _normal );
        }
        else if ( _axis == "Z" )
        {
            // Convert the value to a rotation Matrix
            rotMat = x3dom.fields.SFMatrix4f.rotationX( value );

            // Rotate the normal
            _normal = rotMat.multMatrixPnt( _normal );
        }
 
        updateClipPlane();
        updateProxy();

    };
    
    // FPAV: a function to switch the clip planes on or off
    this.State = function ( )
    {
        if (_enabled == "true" )
        {
            _clipPlane.setAttribute("enabled", "false");
            _enabled = "false";
            _proxyMat.setAttribute("transparency", "1");
        }
        else if (_enabled =="false")
        {
            _clipPlane.setAttribute("enabled", "true");
            _enabled = "true";
            _proxyMat.setAttribute("transparency", "0");
        }
    };

    // A function to deal with axis swapping
    this.Axis = function ( axis )
    {
        _axis = axis;

        _angle = 0;
        
        _distance = 0;
        
        if ( _axis == "X" )
        {
            _normal = new x3dom.fields.SFVec3f(_clipping, 0, 0);
        }
        else if ( _axis == "Y" )
        {
            _normal = new x3dom.fields.SFVec3f(0, _clipping, 0);
            
        }
        else if ( _axis == "Z" )
        {
            _normal = new x3dom.fields.SFVec3f(0, 0, _clipping);
        }

        updateProxy();
        updateClipPlane();
        updateProxyCoordinates();
    };

    // A function to deal with the clipping side change (near/far)
    this.Clipping = function ( clipping )
    {
        _clipping = clipping;

        _angle = 0;
        
        _distance = 0;
        
        if ( _axis == "X" )
        {
            _normal = new x3dom.fields.SFVec3f(_clipping, 0, 0);
        }
        else if ( _axis == "Y" )
        {
            _normal = new x3dom.fields.SFVec3f(0, _clipping, 0);
            
        }
        else if ( _axis == "Z" )
        {
            _normal = new x3dom.fields.SFVec3f(0, 0, _clipping);
        }

        updateProxy();
        updateClipPlane();
    };
    
    // A function to get the volume of the model (???)
    var updateVolume = function ()
    {
        _volume = _runtime.getBBox( clipScope );
    };

    // A function to apply a given state change to the clip plane
    var updateClipPlane = function ()
    {
        if ( _axis == "X" )
        {
            //_clipPlane.setAttribute("plane", _clipping + " 0 0 0");
            _clipPlane.setAttribute("plane", _normal.x + " " + _normal.y + " " + _normal.z + " " + _distance);
        }
        else if ( _axis == "Y" )
        {
            //_clipPlane.setAttribute("plane", "0 " + _clipping + " 0 0");
            _clipPlane.setAttribute("plane", _normal.x + " " + _normal.y + " " + _normal.z + " " + _distance);

        }
        else if ( _axis == "Z" )
        {
            //_clipPlane.setAttribute("plane", "0 0 " + _clipping + " 0");
            _clipPlane.setAttribute("plane", _normal.x + " " + _normal.y + " " + _normal.z + " " + _distance);
        }
    };

    // A function to apply a given state change to the proxy plane
    var updateProxy = function ()
    {
        // FPAV: This function is was not fully correct. If the clip plane is moved AND 
        // rotated, the black "proxy" plane was not tracking the clip plane anymore.
        // The translation vector was incorrect. It was lacking a cosine correction.
        if ( _axis == "X" )
        {
            _proxyTransform.setAttribute("rotation", "0 1 0 " + _angle );
            //_proxyTransform.setAttribute("translation", -_distance * _clipping + " 0 0"); // Original code
            //_proxyTransform.setAttribute("translation", -_distance/Math.cos(_angle) * _clipping + " 0 0"); // Better - but fails if angle=90
        }
        else if ( _axis == "Y" )
        {
        
            _proxyTransform.setAttribute("rotation", "0 0 1 " + _angle );
            //_proxyTransform.setAttribute("translation", "0 " + -_distance  * _clipping + " 0");

        }
        else if ( _axis == "Z" )
        {
            _proxyTransform.setAttribute("rotation", "1 0 0 " + _angle );
            //_proxyTransform.setAttribute("translation", "0 0 " + -_distance * _clipping);

        }
        
        // FPAV: Uglier but reliable ...
        _proxyTransform.setAttribute("translation", -_distance * _normal.x + " " + (-_distance * _normal.y) + " "+ (-_distance  * _normal.z) );
        
    };

    // A function to update the coordinates of the proxy plane
    var updateProxyCoordinates = function ()
    {
        var p0, p1, p2, p3, p4;

        if ( _axis == "X")
        {
            p0 = "0 " + _volume.max.y + " " + _volume.min.z + ", ";
            p1 = "0 " + _volume.min.y + " " + _volume.min.z + ", ";
            p2 = "0 " + _volume.min.y + " " + _volume.max.z + ", ";
            p3 = "0 " + _volume.max.y + " " + _volume.max.z + ", ";
            p4 = "0 " + _volume.max.y + " " + _volume.min.z;

            _proxyCoordinates.setAttribute("point", p0 + p1 + p2 + p3 + p4);
        }
        else if ( _axis == "Y" )
        {
            p0 = _volume.min.x + " 0 " + _volume.max.z + ", ";
            p1 = _volume.min.x + " 0 " + _volume.min.z + ", ";
            p2 = _volume.max.x + " 0 " + _volume.min.z + ", ";
            p3 = _volume.max.x + " 0 " + _volume.max.z + ", ";
            p4 = _volume.min.x + " 0 " + _volume.max.z;

            _proxyCoordinates.setAttribute("point", p0 + p1 + p2 + p3 + p4);
        }
        else if ( _axis == "Z" )
        {
            p0 = _volume.min.x + " " + _volume.max.y + " 0, ";
            p1 = _volume.min.x + " " + _volume.min.y + " 0, ";
            p2 = _volume.max.x + " " + _volume.min.y + " 0, ";
            p3 = _volume.max.x + " " + _volume.max.y + " 0, ";
            p4 = _volume.min.x + " " + _volume.max.y + " 0";

            _proxyCoordinates.setAttribute("point", p0 + p1 + p2 + p3 + p4);
        }
    };

    // A function that creates a clip plane from nothing
    var createClipPlane = function()
    {
        _clipPlane = document.createElement("ClipPlane");
        _clipPlane.setAttribute("enabled",_enabled);
        _clipPlane.setAttribute("plane", _clipping + " 0 0 0");
        _clipPlane.setAttribute("cappingStrength", "0.003");
        _clipPlane.setAttribute("cappingColor", _color);

        _scope.appendChild( _clipPlane );
    };

    // A function that creates a proxy plane from nothing
    var createProxy = function()
    {
        _proxyTransform = document.createElement("Transform");

        var shape = document.createElement("Shape");

        var app = document.createElement("Appearance");

        var mat = document.createElement("Material");
        mat.setAttribute("emissiveColor", _color);
        
        _proxyMat = mat
        
        var line = document.createElement("LineSet");
        line.setAttribute("vertexCount", "5");

        _proxyCoordinates = document.createElement("Coordinate");

        updateProxyCoordinates( _axis );

        _proxyTransform.appendChild( shape );

        shape.appendChild( app );

        app.appendChild( mat );

        shape.appendChild( line );

        line.appendChild( _proxyCoordinates );

        _proxyParent.appendChild( _proxyTransform );
    };

    initialize();
};