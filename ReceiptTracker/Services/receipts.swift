//
//  receipts.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-16.
//

import Foundation

class APIService {
    static let shared = APIService() // singleton instance
    
    func fetchReceipts(completion: @escaping (Result<[Receipt], Error>) -> Void) {
        guard let url = URL(string: "http://192.168.2.18:8000/receipts") else {
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                print("error in deconding data")
                return
            }
            
            if let data = data {
                do {
                    let receipts = try JSONDecoder().decode([Receipt].self, from: data)
                    completion(.success(receipts))
                }
                catch {
                    completion(.failure(error))
                }
            }
        }.resume()
    }
    
    func saveReceipt(receipt: Receipt) {
        // TODO save the receipt to the db
        guard let url = URL(string: "http://192.168.2.18:8000/receipts/") else {
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // save the receipt
        do {
            
            // encode the receipt data
            let jsonData = try JSONEncoder().encode(receipt)
            request.httpBody = jsonData
            
            // try to make a post request
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error trying to make a post request using url \(url): \(error)")
                    return
                }
                
                if let data = data {
                    do {
                        let responseModel = try JSONSerialization.jsonObject(with: data, options: [])
                        print("response model: \(responseModel)")
                    }
                    catch {
                        print("error decoding json: \(error)")
                    }
                }
            }.resume()
        }
        catch {
            print("Error saving the receipt: \(error)")
        }
    }
}
