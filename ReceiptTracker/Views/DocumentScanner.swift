//
//  DocumentScanner.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-07-22.
//

import VisionKit

class ViewController: UIViewController, VNDocumentCameraViewControllerDelegate {
    var scannerAvailable: Bool {
        VNDocumentCameraViewController.isSupported
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    // when you want to show a document scanner, just instantiate a new VNDocumentCameraViewController, assign your delegate, and present it
    func showDocumentScanner() {
        guard VNDocumentCameraViewController.isSupported else { print("Document scanning not supported")
            return
            
        }
        let documentCameraViewController = VNDocumentCameraViewController()
        documentCameraViewController.delegate = self
        present(documentCameraViewController, animated: true)
        
    }

}
