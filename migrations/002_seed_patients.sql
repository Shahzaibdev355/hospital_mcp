INSERT INTO patients
(patient_id, name, age, gender, blood_group, department, admission_date, status)
VALUES
('P1001', 'Ali Raza', 34, 'Male', 'B+', 'Cardiology', '2026-08-20', 'Admitted'),
('P1002', 'Sara Ahmed', 28, 'Female', 'O+', 'Neurology', '2026-08-21', 'Admitted'),
('P1003', 'Hamza Khan', 52, 'Male', 'A+', 'Orthopedics', '2026-08-18', 'Discharged'),
('P1004', 'Ayesha Malik', 41, 'Female', 'AB+', 'Cardiology', '2026-08-22', 'Admitted'),
('P1005', 'Usman Sheikh', 67, 'Male', 'O-', 'General Medicine', '2026-08-15', 'Discharged')
ON CONFLICT (patient_id) DO NOTHING;