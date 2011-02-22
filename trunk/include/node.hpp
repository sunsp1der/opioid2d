
#ifndef NODE_HPP
#define NODE_HPP

#include "util.hpp"

#include <set>

#include "vec.hpp"
#include "mat.hpp"
#include "color.hpp"
#include "director.hpp"
#include "identified.hpp"
#include "num.hpp"
#include <list>

namespace opi2d
{
    class Node;
    class Layer;
    class Physics;
    class Sprite;

    typedef std::list< Node* > Nodes;
   
    class DLLEXPORT Node : public Identified
    {
    public:
        // Constructor
        Node();
        
        // Destructor
        virtual ~Node();

        virtual void Delete();
        virtual void ReUse();
    
        void Place(Layer* layer);
        inline Layer* GetLayer() const { return this->layer; }
        Layer* GetRootLayer() const;
        
        // Node Relation Methods
        Node* AttachTo(Node* parent, bool back=false);
        Node* Detach();
        inline Node* GetParent() const { return this->parent; }
        
        // Overridable callback methods when a new child is added to this node
        virtual void OnAttach(Node* child, bool back);
        virtual void OnDetach(Node* child);
        
        // Traverse the Graph, updating and rendering each Node
        void Traverse(int& zorder);
        
        // Traverse the graph on a free-form layer
        void TraverseFree();
        
        // Override in Node subclasses to do something during graph traversal
        virtual void Enter();
        
        // Render the node on free-form layer traversal
        virtual void EnterFree();
 
        Sprite* Pick(const Vec2& p);
        virtual Sprite* PickSelf(const Vec2& p);
        
        // Attribute Access Methods
        void SetColor(float r=1, float g=1, float b=1, float a=1);
        inline Color& GetColor() { return this->color; }

		inline void SetColorInheritance(bool flag) { this->inherit_color = flag; }
		inline bool GetColorInheritance() const { return this->inherit_color; }

		void ToThisFrame(Vec2& p) const;
		void ToParentFrame(Vec2& p) const;
		void FromThisFrame(Vec2& p) const;
		void FromParentFrame(Vec2& p) const;

        inline const Vec2& GetPos() const
        {
             return this->pos;
        }
        inline Vec2& GetPos()
        {
             return this->pos;
        }
        inline void SetPos(double x, double y)
        {
             this->pos.x = x; this->pos.y = y;
        }
        inline void AddPos(double dx, double dy)
        {
             this->pos.x += dx; this->pos.y += dy;
        }
        
        inline const Vec2& GetWorldPos() const
        {
            if (pos_update_tick != Director::GetInstance()->GetTickID())
            {
                this->update_world_pos();
            }
            return this->realpos;
        }
        
        inline Vec2 GetPosDelta() const
        {
        	return GetWorldPos() - this->oldpos;
        }
        
        inline Vec2 GetWorldVelocity() const
        {
        	double delta = Director::GetInstance()->GetTicker().delta;
        	return this->GetPosDelta() / delta;
        }
        
        inline const Mat9& GetTransformationMatrix() const
        {
            if (pos_update_tick != Director::GetInstance()->GetTickID())
            {
                this->update_world_pos();
            }
            return this->tmat;
        }
        
        inline const Vec2& GetScale() const 
        {
             return this->scale;
        }
        inline Vec2& GetScale()
        {
             return this->scale;
        }
        inline void SetScale(floatval scale)
        {
             this->scale.set(scale,scale);
        }
        inline void SetScale(const Vec2& scale)
        {
            this->scale.set(scale);
        }
        inline const Vec2& GetOffset() const
        {
             return this->offset;
        }
        inline Vec2& GetOffset()
        {
             return this->offset;
        }
        inline floatval GetRotation() const
        {
             return this->rotation;
        }
        inline floatval& GetRotation()
        {
            return this->rotation;
        }
        inline void SetRotation(floatval value)
        {
             this->rotation = value;
        }
        
        Physics* physics;
        
    protected:
        friend class Layer;
        friend class Scene;
            
        static void DeleteNodes(Nodes& nodes);
               
        inline void update_world_pos() const
        {
            int tickid = Director::GetInstance()->GetTickID();
            if (this->parent != NULL)
            {
                if (this->parent->pos_update_tick != tickid)
                {
                    this->parent->update_world_pos();
                }
                this->tmat = this->parent->tmat;
            }
            else
            {
                this->tmat.identity();
            }
            this->transform();
            this->realpos.set(0,0);
            this->tmat.transform(this->realpos);
            this->pos_update_tick = tickid;
        }
        
        inline void transform(Mat9& mat) const
        {
             mat.translate(pos-offset);
             if (rotation != 0) mat.rotate(rotation);
             if (!scale.cmp(1,1)) mat.scale(scale);
             if (!offset.cmp(0,0)) mat.translate(offset);
        }
        inline void transform() const
        {
             transform(tmat);
        }
        
        Layer* layer;
        
        // Transformation attributes
        Vec2 pos;
        Vec2 offset;
        Vec2 scale;
        floatval rotation; // rotation angle in degrees
               
        // Node relationship attributes
        Nodes fChildren;
        Nodes bChildren;
        Node* parent;

        Color color;
        bool inherit_color;

        // Transformation and color accumulation
		mutable Color tcolor;
        mutable Mat9 tmat;
        mutable int zorder;
        mutable Vec2 realpos; // transformed world location
        mutable Vec2 oldpos; // previous world pos
        
        mutable int pos_update_tick;

     };
}

#endif

