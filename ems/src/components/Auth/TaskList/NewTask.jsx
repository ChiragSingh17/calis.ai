import React from 'react'
 const NewTask = ({data}) =>{
  return(
    <div className='h-full flex-shrink-0 w-[300px] p-5 bg-blue-400 rounded-xl'>
            <div className='flex justify-between items-center'>
              <h3 className='bg-red-600 px-3 py-1 rounded'>{data.category}</h3>
              <h4>{data.date}</h4>
           </div>
           <h2 className='mt-5 text-xl font-semibold'>{data.title}</h2>
           <div className='mt-4'>
            <p>{data.description}</p>
                <button className= 'bg-green-500 rounded w-full mt-3'>Accept Task</button>

           </div>
        </div>
  )
 }

 export default NewTask