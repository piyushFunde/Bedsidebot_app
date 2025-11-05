from flask import Blueprint, jsonify, request
from database import db, Patient, PatientRequest, MonitoringSession, SystemAnalytics, get_patient_request_patterns
from datetime import datetime, timedelta
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard_analytics():
    """Get real-time dashboard analytics"""
    try:
        today = datetime.utcnow().date()
        
        # Current statistics
        total_patients = Patient.query.filter_by(is_active=True).count()
        active_monitoring = MonitoringSession.query.filter(MonitoringSession.session_end.is_(None)).count()
        
        # Today's requests
        today_requests = PatientRequest.query.filter(
            func.date(PatientRequest.timestamp) == today
        ).count()
        
        # Emergency requests today
        emergency_requests = PatientRequest.query.filter(
            func.date(PatientRequest.timestamp) == today,
            PatientRequest.request_type == 5
        ).count()
        
        # Request type breakdown for today
        request_breakdown = db.session.query(
            PatientRequest.request_type,
            func.count(PatientRequest.id).label('count')
        ).filter(
            func.date(PatientRequest.timestamp) == today
        ).group_by(PatientRequest.request_type).all()
        
        request_types = {
            1: 'Nurse Calls',
            2: 'Water Requests', 
            3: 'Food Requests',
            4: 'Bathroom Requests',
            5: 'Emergency Calls'
        }
        
        breakdown_data = {}
        for req_type, count in request_breakdown:
            breakdown_data[request_types.get(req_type, 'Unknown')] = count
        
        # Recent requests (last 10)
        recent_requests = PatientRequest.query.order_by(
            PatientRequest.timestamp.desc()
        ).limit(10).all()
        
        recent_data = []
        for req in recent_requests:
            patient = Patient.query.filter_by(patient_id=req.patient_id).first()
            recent_data.append({
                'patient_name': patient.full_name if patient else 'Unknown',
                'request_type': request_types.get(req.request_type, 'Unknown'),
                'timestamp': req.timestamp.strftime('%H:%M'),
                'method': req.request_method,
                'status': req.status
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_patients': total_patients,
                'active_monitoring': active_monitoring,
                'today_requests': today_requests,
                'emergency_requests': emergency_requests,
                'request_breakdown': breakdown_data,
                'recent_requests': recent_data
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@analytics_bp.route('/api/analytics/patient/<patient_id>', methods=['GET'])
def get_patient_analytics(patient_id):
    """Get detailed analytics for a specific patient"""
    try:
        days = request.args.get('days', 7, type=int)
        
        # Get patient info
        patient = Patient.query.filter_by(patient_id=patient_id).first()
        if not patient:
            return jsonify({'status': 'error', 'message': 'Patient not found'}), 404
        
        # Get request patterns
        patterns = get_patient_request_patterns(patient_id, days)
        
        # Get hourly distribution
        hourly_requests = db.session.query(
            func.extract('hour', PatientRequest.timestamp).label('hour'),
            func.count(PatientRequest.id).label('count')
        ).filter(
            PatientRequest.patient_id == patient_id,
            PatientRequest.timestamp >= datetime.utcnow() - timedelta(days=days)
        ).group_by(func.extract('hour', PatientRequest.timestamp)).all()
        
        hourly_data = {str(int(hour)): count for hour, count in hourly_requests}
        
        # Get response time statistics
        response_times = db.session.query(
            PatientRequest.timestamp,
            PatientRequest.response_time
        ).filter(
            PatientRequest.patient_id == patient_id,
            PatientRequest.response_time.isnot(None)
        ).all()
        
        avg_response_time = 0
        if response_times:
            total_time = sum([(resp.response_time - resp.timestamp).total_seconds() / 60 for resp in response_times])
            avg_response_time = total_time / len(response_times)
        
        return jsonify({
            'status': 'success',
            'data': {
                'patient_info': patient.to_dict(),
                'patterns': patterns,
                'hourly_distribution': hourly_data,
                'avg_response_time': round(avg_response_time, 2),
                'analysis_period': f'{days} days'
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@analytics_bp.route('/api/analytics/trends', methods=['GET'])
def get_system_trends():
    """Get system-wide trends and patterns"""
    try:
        days = request.args.get('days', 30, type=int)
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)
        
        # Daily request trends
        daily_trends = db.session.query(
            func.date(PatientRequest.timestamp).label('date'),
            func.count(PatientRequest.id).label('total_requests'),
            func.sum(func.case([(PatientRequest.request_type == 5, 1)], else_=0)).label('emergency_requests')
        ).filter(
            func.date(PatientRequest.timestamp) >= start_date
        ).group_by(func.date(PatientRequest.timestamp)).all()
        
        trend_data = []
        for trend in daily_trends:
            trend_data.append({
                'date': trend.date.isoformat(),
                'total_requests': trend.total_requests,
                'emergency_requests': trend.emergency_requests or 0
            })
        
        # Most active patients
        active_patients = db.session.query(
            PatientRequest.patient_id,
            func.count(PatientRequest.id).label('request_count')
        ).filter(
            PatientRequest.timestamp >= datetime.utcnow() - timedelta(days=days)
        ).group_by(PatientRequest.patient_id).order_by(
            func.count(PatientRequest.id).desc()
        ).limit(5).all()
        
        patient_activity = []
        for patient_id, count in active_patients:
            patient = Patient.query.filter_by(patient_id=patient_id).first()
            patient_activity.append({
                'patient_name': patient.full_name if patient else 'Unknown',
                'patient_id': patient_id,
                'request_count': count
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'daily_trends': trend_data,
                'most_active_patients': patient_activity,
                'analysis_period': f'{days} days'
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@analytics_bp.route('/api/analytics/export', methods=['GET'])
def export_analytics_data():
    """Export analytics data for reporting"""
    try:
        days = request.args.get('days', 30, type=int)
        format_type = request.args.get('format', 'json')
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get all requests in the period
        requests = PatientRequest.query.filter(
            PatientRequest.timestamp >= start_date
        ).all()
        
        export_data = []
        for req in requests:
            patient = Patient.query.filter_by(patient_id=req.patient_id).first()
            export_data.append({
                'timestamp': req.timestamp.isoformat(),
                'patient_id': req.patient_id,
                'patient_name': patient.full_name if patient else 'Unknown',
                'room_number': req.room_number,
                'bed_number': req.bed_number,
                'request_type': req.request_type,
                'request_method': req.request_method,
                'request_message': req.request_message,
                'status': req.status,
                'urgency_level': req.urgency_level,
                'response_time_minutes': ((req.response_time - req.timestamp).total_seconds() / 60) if req.response_time else None
            })
        
        return jsonify({
            'status': 'success',
            'data': export_data,
            'total_records': len(export_data),
            'period': f'{start_date.date()} to {end_date.date()}'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500