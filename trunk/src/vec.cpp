
#include "vec.hpp"
#include "opivm.hpp"

namespace opi2d
{
    void Vec2::VM_GetProp(ExecFrame* f, int idx)
    {
    	
        switch(idx)
        {
        	case 0: // x
        	    f->pushf(this->x);
        	    break;
        	case 1: // y 
        		f->pushf(this->y);
        		break;
        	case 2: // length
        		f->pushf(this->length());
        		break;
        	case 3: // direction
        		f->pushf(this->direction());
        		break;
        }
    	
    }

    void Vec2::VM_SetProp(ExecFrame* f, int idx)
    {
    	floatval v;
        switch(idx)
        {
        	case 0: // x
        		v = f->popf();
        	    this->x = v;
        	    break;
        	case 1: // y
        		v = f->popf();
        		this->y = v;
        		break;
        	case 2: // length
        		v = f->popf();
        		this->set_length(v);
        	case 3: // direction
        		v = f->popf();
        		this->set_direction(v);
        }
    }

    void Vec2::VM_MetCall(ExecFrame* f, int idx)
    {
    	floatval x,y;
    	Vec2* v;
    	switch(idx)
    	{
    		case 0: // set(float,float)
    		    y = f->popf();
    			x = f->popf();
    			this->set(x,y);
    			break;
    		case 1: // set(vec)
    			v = f->popv();
    			this->set(*v);
    			break;
    		case  2: // add(f,f)
    		    y = f->popf();
    			x = f->popf();
    			this->add(x,y);
    			break;
    		case  3: // add(v)
    			v = f->popv();
    			this->add(*v);
    			break;
    		case  4: // sub(f,f)
    		    y = f->popf();
    			x = f->popf();
    			this->sub(x,y);
    			break;
    		case  5: // sub(v)
    			v = f->popv();
				this->sub(*v);
				break;
    		case  6: // mul(f)
    			x = f->popf();
    			this->mul(x);
    			break;
    		case  7: // mul(f,f)
    		    y = f->popf();
    			x = f->popf();
    			this->mul(x,y);
    			break;
    		case  8: // mul(v)
    			v = f->popv();
    			this->mul(*v);
    			break;
    		case  9: // div(f)
    			x = f->popf();
    			this->div(x);
    			break;
    		case 10: // div(f,f)
    		    y = f->popf();
    			x = f->popf();
    			this->div(x,y);
    			break;
    		case 11: // div(v)
    			v = f->popv();
    			this->div(*v);
    			break;
    	}
    }	

}
