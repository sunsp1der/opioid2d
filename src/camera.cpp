
#include "camera.hpp"
#include "mat.hpp"
#include "display.hpp"
#include "layer.hpp"

namespace opi2d
{
	Camera::Camera()
	: alignToParent(false)
	{
	}
	
	void Camera::SetAlign(bool flag)
	{
		this->alignToParent = flag;
	}
	
	bool Camera::GetAlign() const
	{
		return this->alignToParent;
	}
	
	void Camera::Adjust()
	{
		if (this->parent != NULL)
		{
			this->GetPos().set(this->parent->GetWorldPos());
			if (this->alignToParent)
			{
				Vec2 v1(0.0, 0.0);
				Vec2 v2(0.0, -1.0);
				this->parent->GetTransformationMatrix().transform(v1);
				this->parent->GetTransformationMatrix().transform(v2);
				this->SetRotation(-(v2-v1).direction());
			}
		}
	}
	
	void Camera::ScreenToWorld(Vec2& p) const
	{
        const Vec2& units = Display::GetInstance()->GetViewSize();
        const int ux = (int)(units.x / 2);
        const int uy = (int)(units.y / 2);
		Mat9 m;
		m.identity();
		m.translate(pos);
		m.rotate(-rotation);
		m.scale(1.0/scale.x, 1.0/scale.y);
		m.translate(-ux,-uy);
		m.transform(p);
	}

	void Camera::ScreenToWorld(Vec2& p, Layer* layer) const
	{
        const Vec2& units = Display::GetInstance()->GetViewSize();
        const int ux = (int)(units.x / 2);
        const int uy = (int)(units.y / 2);
		Mat9 m;
		m.identity();
		m.translate(pos * layer->camera_offset);
		m.rotate(-rotation * layer->camera_rotation);
	    floatval x = layer->camera_zoom * (scale.x-1.0) + 1.0;
	    floatval y = layer->camera_zoom * (scale.y-1.0) + 1.0;		
		m.scale(1.0/x, 1.0/y);
		m.translate(-ux,-uy);
		m.transform(p);		
	}

}
